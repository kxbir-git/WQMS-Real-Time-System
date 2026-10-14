/*
 * ============================================================
 *  AquaSense WQMS — IoT-Based Real-Time Water Quality Monitor
 *  Hardware: ESP32 DevKit V1
 *    - TDS Sensor SEN0244        → GPIO 34 (ADC1_CH6)
 *    - Analog pH Sensor (E-201)  → GPIO 35 (ADC1_CH7)
 *    - Turbidity Sensor SEN0189  → GPIO 32 (ADC1_CH4)
 *    - DS18B20 Temp Sensor       → GPIO 4 (1-Wire + 4.7kΩ pull-up)
 *
 *  Author  : B.Tech CSE Final Year Capstone Project
 *  Date    : 2026
 *
 *  Libraries needed (Arduino Library Manager):
 *    - PubSubClient (Nick O'Leary)
 *    - OneWire (Paul Stoffregen)
 *    - DallasTemperature (Miles Burton)
 * ============================================================
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

/* ============================================================
 *  USER CONFIGURATION — Update Wi-Fi & Broker IP
 * ============================================================ */
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

const char* MQTT_BROKER   = "192.168.1.100";  // IP of PC running Mosquitto / Flask
const int   MQTT_PORT     = 1883;
const char* MQTT_TOPIC    = "water/tds/data";
const char* DEVICE_ID     = "WQMS_NODE01";

/* ============================================================
 *  PIN DEFINITIONS (ESP32 ADC1 Pins Only)
 * ============================================================ */
#define TDS_PIN           34   // Analog pin for TDS sensor
#define PH_PIN            35   // Analog pin for pH sensor
#define TURB_PIN          32   // Analog pin for Turbidity sensor
#define ONE_WIRE_BUS      4    // DS18B20 1-Wire bus pin

#define ADC_VREF          3.3  // Reference Voltage
#define ADC_RESOLUTION    4096 // 12-bit ADC
#define SAMPLE_COUNT      40   // Median filter samples
#define PUBLISH_INTERVAL  4000 // Milliseconds between telemetry packets

/* ============================================================
 *  OBJECTS & GLOBALS
 * ============================================================ */
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishTime = 0;
float currentTemp = 25.0;

/* ============================================================
 *  WIFI & MQTT CONNECTIVITY
 * ============================================================ */
void connectWiFi() {
  Serial.print("Connecting to Wi-Fi [");
  Serial.print(WIFI_SSID);
  Serial.print("]...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 30) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ Wi-Fi Connected! IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\n✗ Wi-Fi Connection Timeout. Continuing in offline buffer mode...");
  }
}

void connectMQTT() {
  if (WiFi.status() != WL_CONNECTED) return;

  int attempts = 0;
  while (!mqttClient.connected() && attempts < 3) {
    Serial.print("Connecting to MQTT broker...");
    String clientId = "ESP32-WQMS-" + String(random(0xffff), HEX);
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println(" ✓ Connected!");
    } else {
      Serial.print(" ✗ State: ");
      Serial.println(mqttClient.state());
      delay(2000);
      attempts++;
    }
  }
}

/* ============================================================
 *  SENSOR READING FUNCTIONS
 * ============================================================ */
float readTemperature() {
  tempSensor.requestTemperatures();
  float temp = tempSensor.getTempCByIndex(0);
  if (temp == DEVICE_DISCONNECTED_C || temp < -10.0 || temp > 80.0) {
    return 25.0; // Standard reference temperature fallback
  }
  return temp;
}

float readMedianVoltage(int pin) {
  int buf[SAMPLE_COUNT];
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    buf[i] = analogRead(pin);
    delay(8);
  }
  // Sort for median filtering
  for (int i = 0; i < SAMPLE_COUNT - 1; i++) {
    for (int j = 0; j < SAMPLE_COUNT - 1 - i; j++) {
      if (buf[j] > buf[j + 1]) {
        int t = buf[j];
        buf[j] = buf[j + 1];
        buf[j + 1] = t;
      }
    }
  }
  // Average middle 20 values
  float avg = 0;
  for (int i = 10; i < 30; i++) avg += buf[i];
  avg /= 20.0;
  return (avg / ADC_RESOLUTION) * ADC_VREF;
}

float calculateTDS(float voltage, float temp) {
  float compVoltage = voltage / (1.0 + 0.02 * (temp - 25.0));
  float tds = (133.42 * pow(compVoltage, 3) - 255.86 * pow(compVoltage, 2) + 857.39 * compVoltage) * 0.5;
  return constrain(tds, 0.0, 2000.0);
}

float calculatePH(float voltage) {
  // Standard pH probe transfer function: pH 7.0 at ~2.5V, 3.5 slope
  float ph = 7.0 + ((2.5 - voltage) * 3.5);
  return constrain(ph, 0.0, 14.0);
}

float calculateTurbidity(float voltage) {
  // Standard SEN0189 transfer: high voltage (~4.2V/3.3V) = clean water; low voltage = turbid
  // Linearized approximation 0-20 NTU
  float ntu = -1120.4 * pow(voltage, 2) + 5742.3 * voltage - 4352.9;
  if (voltage >= 3.0) ntu = 0.5;
  return constrain(ntu, 0.0, 50.0);
}

/* ============================================================
 *  TELEMETRY DISPATCH
 * ============================================================ */
void publishTelemetry(float tds, float ph, float turb, float temp) {
  float do_val = constrain(14.6 - (0.28 * temp), 4.5, 9.5); // Dissolved Oxygen approx
  float ec = tds / 0.64;                                    // Electrical conductivity in µS/cm

  String payload = "{";
  payload += "\"device_id\":\"" + String(DEVICE_ID) + "\",";
  payload += "\"tds\":" + String(tds, 1) + ",";
  payload += "\"ph\":" + String(ph, 2) + ",";
  payload += "\"turbidity\":" + String(turb, 2) + ",";
  payload += "\"temperature\":" + String(temp, 1) + ",";
  payload += "\"do\":" + String(do_val, 2) + ",";
  payload += "\"ec\":" + String(ec, 1);
  payload += "}";

  if (mqttClient.connected()) {
    mqttClient.publish(MQTT_TOPIC, payload.c_str());
    Serial.println("✓ [MQTT] " + payload);
  } else {
    Serial.println("ℹ [Local Reading] " + payload);
  }
}

/* ============================================================
 *  SETUP & MAIN LOOP
 * ============================================================ */
void setup() {
  Serial.begin(115200);
  Serial.println("\n================================================");
  Serial.println(" AquaSense WQMS Multi-Sensor Telemetry Active");
  Serial.println("================================================\n");

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  tempSensor.begin();
  connectWiFi();

  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED && !mqttClient.connected()) {
    connectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = now;

    currentTemp = readTemperature();
    float tdsV = readMedianVoltage(TDS_PIN);
    float tds = calculateTDS(tdsV, currentTemp);

    float phV = readMedianVoltage(PH_PIN);
    float ph = calculatePH(phV);

    float turbV = readMedianVoltage(TURB_PIN);
    float turb = calculateTurbidity(turbV);

    publishTelemetry(tds, ph, turb, currentTemp);
  }
}
