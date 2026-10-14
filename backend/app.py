# =============================================================
#  app.py — Full-Stack Flask Server & Multi-Parameter REST API
#
#  Hardware-Only Mode:
#    - Background simulation is DISABLED.
#    - System monitors actual ESP32 telemetry timestamp.
#    - If no packet is received within 12 seconds, the dashboard
#      enters Standby / Hardware Disconnected mode.
# =============================================================

import os
import io
import csv
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from sqlalchemy import func, desc

import config
from database import init_db, get_session, WaterQualityReading
from alert_service import evaluate_parameter_status, calculate_wqi, log_alert
from mqtt_subscriber import start_mqtt_subscriber

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Ensure database tables exist
init_db()

# Start background MQTT subscriber
start_mqtt_subscriber()

# Maximum age of sensor reading (seconds) before marking hardware offline
HARDWARE_TIMEOUT_SECONDS = 12.0


# -------------------------------------------------------------
# Static Frontend Serving
# -------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)


# -------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------

@app.route("/api/latest", methods=["GET"])
def get_latest_reading():
    """
    Returns the most recent reading from the database.
    Strictly verifies whether data arrived recently from physical hardware.
    """
    session = get_session()
    try:
        latest = session.query(WaterQualityReading).order_by(desc(WaterQualityReading.timestamp)).first()
        if not latest:
            return jsonify({
                "status": "offline",
                "is_live": False,
                "message": "Hardware disconnected. Waiting for ESP32 sensor stream..."
            }), 200

        # Calculate time difference between now and the latest reading
        age_seconds = (datetime.utcnow() - latest.timestamp).total_seconds()
        is_live = age_seconds <= HARDWARE_TIMEOUT_SECONDS

        res = latest.to_dict()
        res["is_live"] = is_live
        res["seconds_ago"] = round(age_seconds, 1)

        if not is_live:
            res["status"] = "offline"
            res["message"] = f"Hardware disconnected (last seen {round(age_seconds)}s ago)."

        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/api/history", methods=["GET"])
def get_history():
    """Returns historical readings for trend charts."""
    hours = request.args.get("hours", default=24, type=float)
    since_time = datetime.utcnow() - timedelta(hours=hours)

    session = get_session()
    try:
        readings = (
            session.query(WaterQualityReading)
            .filter(WaterQualityReading.timestamp >= since_time)
            .order_by(WaterQualityReading.timestamp.asc())
            .all()
        )
        return jsonify([r.to_dict() for r in readings]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns today's min, max, avg for TDS, pH, Turbidity, DO, EC, Temp."""
    session = get_session()
    try:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        query = session.query(
            func.min(WaterQualityReading.tds_value).label("min_tds"),
            func.max(WaterQualityReading.tds_value).label("max_tds"),
            func.avg(WaterQualityReading.tds_value).label("avg_tds"),
            func.avg(WaterQualityReading.ph_value).label("avg_ph"),
            func.avg(WaterQualityReading.turbidity).label("avg_turb"),
            func.avg(WaterQualityReading.wqi_value).label("avg_wqi"),
            func.count(WaterQualityReading.id).label("count")
        ).filter(WaterQualityReading.timestamp >= today_start).first()

        count = query.count if query else 0
        if count == 0:
            return jsonify({
                "min": 0.0, "max": 0.0, "avg": 0.0,
                "avg_ph": 7.0, "avg_turb": 1.0, "avg_wqi": 90.0,
                "count": 0
            }), 200

        return jsonify({
            "min": round(float(query.min_tds), 1) if query.min_tds is not None else 0.0,
            "max": round(float(query.max_tds), 1) if query.max_tds is not None else 0.0,
            "avg": round(float(query.avg_tds), 1) if query.avg_tds is not None else 0.0,
            "avg_ph": round(float(query.avg_ph), 2) if query.avg_ph is not None else 7.0,
            "avg_turb": round(float(query.avg_turb), 2) if query.avg_turb is not None else 1.0,
            "avg_wqi": round(float(query.avg_wqi), 1) if query.avg_wqi is not None else 90.0,
            "count": count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    """Returns the most recent contamination alert readings."""
    session = get_session()
    try:
        alerts = (
            session.query(WaterQualityReading)
            .filter(WaterQualityReading.status.in_(["Warning", "Unsafe"]))
            .order_by(desc(WaterQualityReading.timestamp))
            .limit(25)
            .all()
        )
        return jsonify([a.to_dict() for a in alerts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/api/sensor/data", methods=["POST"])
def ingest_sensor_http():
    """
    Direct HTTP Ingestion endpoint for ESP32.
    Payload: {"device_id": "ESP32_NODE", "tds": 250, "ph": 7.2, "turbidity": 1.5, "temperature": 25.0, "do": 7.4, "ec": 390}
    """
    try:
        data = request.get_json(force=True) or {}
        device_id = data.get("device_id", "ESP32_NODE")
        tds_val   = float(data.get("tds", data.get("tds_value", 0.0)))
        ph_val    = float(data.get("ph", data.get("ph_value", 7.0)))
        turb_val  = float(data.get("turbidity", data.get("turb", 0.5)))
        temp_val  = float(data.get("temperature", data.get("temp", 25.0)))
        do_val    = float(data.get("do", data.get("do_value", 7.0)))
        ec_val    = float(data.get("ec", data.get("ec_value", tds_val / 0.64 if tds_val > 0 else 0.0)))

        overall_status, _ = evaluate_parameter_status(tds_val, ph_val, turb_val, temp_val, do_val, ec_val)
        wqi = calculate_wqi(tds_val, ph_val, turb_val, do_val, ec_val)

        session = get_session()
        try:
            reading = WaterQualityReading(
                device_id=device_id,
                tds_value=tds_val,
                ph_value=ph_val,
                turbidity=turb_val,
                temperature=temp_val,
                do_value=do_val,
                ec_value=ec_val,
                wqi_value=wqi,
                status=overall_status,
                timestamp=datetime.utcnow()
            )
            session.add(reading)
            session.commit()
            return jsonify({"status": "success", "reading": reading.to_dict()}), 201
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/system/reset", methods=["POST"])
def reset_database():
    """Clears all previous records so screen starts from a completely fresh state."""
    session = get_session()
    try:
        session.query(WaterQualityReading).delete()
        session.commit()
        return jsonify({"message": "Database reset successfully. Ready for clean hardware stream."}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    """Export all records to CSV."""
    session = get_session()
    try:
        readings = session.query(WaterQualityReading).order_by(WaterQualityReading.timestamp.asc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Device ID", "TDS (ppm)", "pH", "Turbidity (NTU)",
            "Temperature (°C)", "DO (mg/L)", "EC (µS/cm)", "WQI Score", "Status", "Timestamp"
        ])

        for r in readings:
            writer.writerow([
                r.id, r.device_id, r.tds_value, r.ph_value, r.turbidity,
                r.temperature, r.do_value, r.ec_value, r.wqi_value, r.status,
                r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ])

        output.seek(0)
        filename = f"water_quality_readings_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    finally:
        session.close()


if __name__ == "__main__":
    print("==================================================")
    print(" AquaSense WQMS — Live Hardware Mode Active")
    print(f" URL: http://localhost:{config.FLASK_PORT}")
    print(" Waiting for real ESP32 hardware packets...")
    print("==================================================")
    app.run(host="0.0.0.0", port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
