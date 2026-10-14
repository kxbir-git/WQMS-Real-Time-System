# =============================================================
#  mock_sensor.py — Multi-Parameter Sensor Simulator
#
#  Simulates 6 parameters:
#    1. TDS (Total Dissolved Solids - ppm)
#    2. pH (Acidity / Alkalinity: 0-14)
#    3. Turbidity (Cloudiness: NTU)
#    4. Temperature (°C)
#    5. Dissolved Oxygen (DO: mg/L)
#    6. Electrical Conductivity (EC: µS/cm)
#
#  Smart Transport:
#    - Attempts MQTT first (localhost:1883)
#    - If MQTT broker is not running, falls back automatically
#      to direct Flask HTTP POST (http://localhost:5000/api/sensor/data)
# =============================================================

import time
import json
import random
import urllib.request
import urllib.error
import paho.mqtt.client as mqtt

import config

HTTP_ENDPOINT = f"http://localhost:{config.FLASK_PORT}/api/sensor/data"

def run_mock_sensor():
    print("=============================================================")
    print(" Multi-Parameter Water Quality Sensor Simulator")
    print(" Parameters: pH, TDS, Turbidity, Temp, DO, EC")
    print("=============================================================\n")

    mqtt_client = None
    use_mqtt = False

    # Attempt MQTT Connection
    try:
        try:
            mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="WQMS_Simulator")
        except AttributeError:
            mqtt_client = mqtt.Client(client_id="WQMS_Simulator")

        mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT, 5)
        mqtt_client.loop_start()
        use_mqtt = True
        print(f"[OK] Connected to MQTT Broker ({config.MQTT_BROKER}:{config.MQTT_PORT})")
    except Exception as e:
        print(f"[NOTE] Local Mosquitto MQTT broker not detected ({e}).")
        print(f"[OK] Using Automatic HTTP Direct Ingestion: {HTTP_ENDPOINT}")
        use_mqtt = False

    print("\nStarting live streaming every 4 seconds. Press Ctrl+C to stop.\n")

    base_tds = 235.0
    base_ph = 7.30
    base_turb = 1.3
    base_temp = 24.5
    base_do = 7.5

    cycle = 0
    try:
        while True:
            cycle += 1

            # Introduce realistic sensor values with occasional spikes to test alert system
            if cycle % 25 == 0:
                # Deliberate contamination anomaly (>900 TDS, alkaline pH, high turbidity)
                tds_val  = round(random.uniform(920.0, 1150.0), 1)
                ph_val   = round(random.uniform(8.9, 9.4), 2)
                turb_val = round(random.uniform(12.0, 22.0), 2)
                do_val   = round(random.uniform(3.0, 3.8), 2)
                temp_val = round(random.uniform(28.0, 33.0), 1)
            elif cycle % 12 == 0:
                # Moderate warning spike
                tds_val  = round(random.uniform(530.0, 680.0), 1)
                ph_val   = round(random.uniform(6.1, 6.4), 2)
                turb_val = round(random.uniform(5.5, 7.8), 2)
                do_val   = round(random.uniform(4.2, 4.9), 2)
                temp_val = round(random.uniform(25.5, 27.5), 1)
            else:
                # Normal high-quality drinking water
                tds_val  = round(base_tds + random.uniform(-12.0, 15.0), 1)
                ph_val   = round(base_ph + random.uniform(-0.15, 0.15), 2)
                turb_val = round(max(0.3, base_turb + random.uniform(-0.25, 0.35)), 2)
                do_val   = round(max(5.0, base_do + random.uniform(-0.3, 0.3)), 2)
                temp_val = round(base_temp + random.uniform(-0.4, 0.4), 1)

            # Approximate EC from TDS (EC in µS/cm ≈ TDS / 0.64)
            ec_val = round(tds_val / 0.64 + random.uniform(-6.0, 6.0), 1)

            payload = {
                "device_id": "WQMS_SIM_01",
                "tds": tds_val,
                "ph": ph_val,
                "turbidity": turb_val,
                "temperature": temp_val,
                "do": do_val,
                "ec": ec_val
            }

            json_str = json.dumps(payload)

            if use_mqtt and mqtt_client:
                mqtt_client.publish(config.MQTT_TOPIC, json_str)
                print(f"[MQTT → {config.MQTT_TOPIC}] {json_str}")
            else:
                # Direct HTTP POST
                try:
                    req = urllib.request.Request(
                        HTTP_ENDPOINT,
                        data=json_str.encode("utf-8"),
                        headers={"Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        pass
                    print(f"[HTTP POST → API] {json_str}")
                except Exception as http_err:
                    print(f"[HTTP Warning] Flask server offline or busy ({http_err}). Start `python app.py`.")

            time.sleep(4)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")
    finally:
        if use_mqtt and mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

if __name__ == "__main__":
    run_mock_sensor()
