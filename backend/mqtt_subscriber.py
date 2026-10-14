# =============================================================
#  mqtt_subscriber.py — Multi-Parameter MQTT Ingestion
# =============================================================

import json
import logging
import threading
import paho.mqtt.client as mqtt

import config
from database import get_session, WaterQualityReading
from alert_service import evaluate_parameter_status, calculate_wqi, log_alert

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mqtt_subscriber")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info(f"Connected to MQTT Broker at {config.MQTT_BROKER}:{config.MQTT_PORT}")
        client.subscribe(config.MQTT_TOPIC)
        logger.info(f"Subscribed to topic: {config.MQTT_TOPIC}")
    else:
        logger.warning(f"MQTT Broker connection returned code: {rc}")


def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)

        device_id = data.get("device_id", "WQMS_NODE01")
        tds_val   = float(data.get("tds_value", data.get("tds", 250.0)))
        temp_val  = float(data.get("temperature", data.get("temp", 24.5)))
        ph_val    = float(data.get("ph_value", data.get("ph", 7.2)))
        turb_val  = float(data.get("turbidity", data.get("turb", 1.5)))
        do_val    = float(data.get("do_value", data.get("do", 7.2)))
        ec_val    = float(data.get("ec_value", data.get("ec", tds_val / 0.64 if tds_val > 0 else 380.0)))

        overall_status, sub_statuses = evaluate_parameter_status(
            tds_val, ph_val, turb_val, temp_val, do_val, ec_val
        )
        wqi = calculate_wqi(tds_val, ph_val, turb_val, do_val, ec_val)

        log_alert(device_id, tds_val, overall_status, f"pH={ph_val}, Turb={turb_val}")

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
                status=overall_status
            )
            session.add(reading)
            session.commit()
            logger.info(f"Ingested Reading: TDS={tds_val}ppm, pH={ph_val}, Turb={turb_val}NTU, DO={do_val}mg/L, WQI={wqi}")
        except Exception as db_err:
            session.rollback()
            logger.error(f"Database error: {db_err}")
        finally:
            session.close()

    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")


def start_mqtt_subscriber():
    """Starts background MQTT thread with safe fallback if broker is offline."""
    def run_loop():
        try:
            # Use safe client instantiation compatible with all paho versions
            try:
                client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            except AttributeError:
                client = mqtt.Client()

            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            logger.info(f"MQTT Broker currently unavailable ({e}). HTTP ingestion API remains fully active.")

    t = threading.Thread(target=run_loop, daemon=True, name="MQTT_Subscriber")
    t.start()
    return t
