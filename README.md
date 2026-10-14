# AquaSense WQMS — IoT-Based Real-Time Multi-Parameter Water Quality Monitoring System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hardware: ESP32](https://img.shields.io/badge/Hardware-ESP32%20DevKit%20V1-blue)](https://www.espressif.com/)
[![Backend: Flask](https://img.shields.io/badge/Backend-Python%20Flask-green)](https://flask.palletsprojects.com/)
[![Protocol: MQTT](https://img.shields.io/badge/Protocol-MQTT%203.1.1-orange)](https://mqtt.org/)
[![Database: SQLite](https://img.shields.io/badge/Database-SQLite%203-lightgrey)](https://www.sqlite.org/)
[![Standards: WHO & BIS](https://img.shields.io/badge/Standards-BIS%20IS%2010500%3A2012-red)](https://bis.gov.in/)

> **B.Tech Computer Science & Engineering — Final Year Capstone Project**  
> Developed as an intensive **15-Day Sprint** by a collaborative **4-Member Team**.

---

## 1. Project Abstract

Drinking water contamination poses acute and chronic global health hazards, with conventional laboratory testing suffering from high turnaround latency and lack of continuous temporal visibility. **AquaSense WQMS** is an industrial-grade, full-stack Internet of Things (IoT) monitoring infrastructure engineered to perform real-time, in-situ assessment of **6 critical physicochemical water quality indicators**:
1. **Total Dissolved Solids (TDS)** — ppm (SEN0244 Analog Probe)
2. **pH Level** — Acidic/Alkaline equilibrium (E-201-C Glass Probe)
3. **Turbidity** — Suspended particulate cloudiness in NTU (SEN0189 Optical Sensor)
4. **Water Temperature** — °C with thermal compensation (DS18B20 1-Wire Probe)
5. **Dissolved Oxygen (DO)** — Aeration level in mg/L
6. **Electrical Conductivity (EC)** — Ionic concentration in µS/cm

The system edge layer utilizes an **ESP32 microcontroller** with a 40-sample median filtering algorithm that eliminates sensor noise and transmits JSON payloads over lightweight **MQTT** (or direct HTTP ingestion) to a local **Python Flask** server. Records are cataloged in an **SQLite** database via SQLAlchemy ORM, and evaluated against a deterministic **Water Quality Index (WQI)** engine matching **WHO** and **Bureau of Indian Standards (BIS IS 10500:2012)** criteria. The client presents an ultra-responsive light-themed dashboard featuring **6 dedicated visual speedometer and dial meters**, historical trend waveforms, automated contamination alerts, and one-click CSV audit export.

---

## 2. Project Team & Work Distribution (4 Members)

This capstone project was planned, executed, and validated collaboratively over a structured 15-day development sprint. Responsibility domains were categorized according to specialized engineering disciplines:

```text
========================================================================================
                          PROJECT WORK DISTRIBUTION MATRIX
========================================================================================
 TEAM MEMBER           ROLE                           PRIMARY DELIVERABLES
----------------------------------------------------------------------------------------
 Member 1              Hardware & Embedded Systems    • ESP32 Pinout & Analog ADC1 wiring
                       Lead                           • Sensor Interfacing (TDS, pH, Turbidity, DS18B20)
                                                      • C++ Firmware (`tds_sensor.ino`)
                                                      • 40-Sample Median Filtering & Polynomial Fitting
----------------------------------------------------------------------------------------
 Member 2              Backend Architecture &         • Flask RESTful API Engine (`app.py`)
                       Protocols Lead                 • MQTT Broker Setup (Eclipse Mosquitto)
                                                      • Background Ingestion Thread (`mqtt_subscriber.py`)
                                                      • Dual Transport Fallback (Direct HTTP API)
----------------------------------------------------------------------------------------
 Member 3              Frontend & UI/UX Developer     • Responsive Single-Page Dashboard (`index.html`)
                                                      • Custom SVG Speedometer & Precision Dial Meters
                                                      • Light White Modern Design System (`style.css`)
                                                      • Chart.js Multi-Parameter Waveforms (`script.js`)
----------------------------------------------------------------------------------------
 Member 4              Database, QA & Validation      • SQLAlchemy ORM Schema & Migrations (`database.py`)
                       Specialist                     • Rule-based WQI Formulation & Alerts (`alert_service.py`)
                                                      • 3-Sample Laboratory Testing Protocol
                                                      • CSV Export Streaming & Documentation Lead
========================================================================================
```

---

## 3. 15-Day Development Sprint Timeline

```text
[Day 1-3] Requirements & Sensor BOM ────► [Day 4-7] Firmware & Circuit Assembly
                                                               │
[Day 14-15] Testing, Audit & Push ◄──── [Day 11-13] Frontend ◄──┴──► [Day 8-10] Backend & WQI
```

| Sprint Phase | Timeline | Key Engineering Milestones |
|---|---|---|
| **Phase 1: Architecture & Feasibility** | **Days 1 – 3** | • Review WHO & BIS IS 10500:2012 drinking water standards.<br>• Component selection & procurement (BOM optimization under ₹3,100).<br>• Protocol benchmarking: MQTT vs HTTP for IoT battery and latency trade-offs. |
| **Phase 2: Embedded Firmware & Prototyping** | **Days 4 – 7** | • Breadboard assembly of ESP32 DevKit V1 with analog sensors on ADC1 channels.<br>• Temperature compensation algorithm implementation for TDS and pH probes.<br>• 40-sample bubble-sort median filter development to suppress electrical noise.<br>• Mosquitto MQTT broker configuration on localhost:1883. |
| **Phase 3: Backend API & WQI Engine** | **Days 8 – 10** | • Python 3.10+ virtual environment and SQLAlchemy ORM database creation.<br>• Background multi-threaded subscriber (`mqtt_subscriber.py`) with auto-reconnection.<br>• Rule-based threshold classification (`alert_service.py`) and WQI computation.<br>• REST endpoints: `/api/latest`, `/api/history`, `/api/stats`, `/api/export/csv`. |
| **Phase 4: Responsive Frontend Console** | **Days 11 – 13** | • Light white modern UI (#FFFFFF cards, #F7F9FC canvas, #2E86DE accents).<br>• Engineering of 6 SVG speedometers/dials with smooth cubic-bezier needle easing.<br>• Perfectly centered WQI circular progress ring with status pills.<br>• Chart.js interactive historical waveforms with parameter switching tabs.<br>• Responsive mobile/tablet/desktop media query optimization. |
| **Phase 5: Laboratory Testing & Project Audit** | **Days 14 – 15** | • Real-world 3-sample validation (RO Filtered, Municipal Tap, Saline Contaminated).<br>• Standby/Hardware-Only stream validation with 12-second auto-disconnect watchdog.<br>• CSV audit export verification and capstone presentation report finalization. |

---

## 4. Hardware Bill of Materials (BOM)

| S.No | Component | Specification | Quantity | Approx. Cost (INR) |
|:---:|---|---|:---:|:---:|
| 1 | **ESP32 DevKit V1** | 30-Pin Dual-Core 240MHz Wi-Fi + BLE Microcontroller | 1 | ₹450 |
| 2 | **Analog TDS Sensor** | DFRobot SEN0244 Probe & Signal Conditioning Board | 1 | ₹550 |
| 3 | **Analog pH Sensor Kit** | E-201-C BNC Glass Electrode + Amplifier Board | 1 | ₹1,200 |
| 4 | **Optical Turbidity Sensor** | SEN0189 Optical Infrared Transmittance Module | 1 | ₹450 |
| 5 | **Waterproof Temperature** | Maxim DS18B20 1-Wire Digital Thermal Probe | 1 | ₹180 |
| 6 | **Pull-up Resistor** | 4.7 kΩ Metal Film Resistor (for 1-Wire Bus) | 1 | ₹5 |
| 7 | **Prototyping & Power** | 400-Point Breadboard, Jumper Wires, 5V/2A Adapter | 1 Set | ₹250 |
| **Total** | | | | **~ ₹3,085** |

---

## 5. Circuit Schematic & Pin Assignment

```text
               +-------------------------------------------+
               |              ESP32 DevKit V1              |
               |                                           |
               |  3V3   GND   GPIO34   GPIO35   GPIO32   GPIO4 |
               +---+-----+------+-------+--------+---------+-+
                   |     |      |       |        |         |
                   |     |      |       |        |         +-- (1-Wire Data + 4.7kΩ to 3V3)
                   |     |      |       |        +-- Turbidity AOUT (Pin 32)
                   |     |      |       +----------- pH AOUT (Pin 35)
                   |     |      +------------------- TDS AOUT (Pin 34)
                   |     |
             3.3V  |     | GND Rail
            Rail   v     v
```

> **Critical Note on ESP32 ADCs**: Always wire analog sensors to **ADC1 channels** (GPIO 32, 33, 34, 35, 36, 39). ADC2 cannot be sampled when Wi-Fi is transmitting!

| Sensor | Sensor Pin | ESP32 GPIO | Channel Type | Operating Voltage |
|---|---|---|---|---|
| **TDS Sensor** | AOUT | GPIO 34 | ADC1_CH6 (Analog) | 3.3V DC |
| **pH Sensor** | AOUT | GPIO 35 | ADC1_CH7 (Analog) | 3.3V DC |
| **Turbidity Sensor** | AOUT | GPIO 32 | ADC1_CH4 (Analog) | 3.3V DC |
| **DS18B20 Temp** | DATA (Yellow) | GPIO 4 | 1-Wire Digital (Pull-up 4.7kΩ) | 3.3V DC |
| **All Sensors** | VCC | 3V3 | Power Bus | 3.3V DC |
| **All Sensors** | GND | GND | Common Ground | 0V |

---

## 6. Software Architecture

```text
[Water Samples (RO / Tap / Contaminated)]
                   │
                   ▼
  [Sensors: TDS + pH + Turbidity + Temp]
                   │
         (Analog / 1-Wire ADC)
                   ▼
        [ESP32 Microcontroller]
  • 40-Sample Bubble-Sort Median Filter
  • Temperature Compensation Equation
  • JSON Formatter & Wi-Fi Client
                   │
      ┌────────────┴────────────┐
      ▼                         ▼
 [MQTT: Port 1883]       [Direct HTTP Ingestion]
 Topic: water/tds/data   POST /api/sensor/data
      └────────────┬────────────┘
                   ▼
      [Python 3.10+ Flask Server]
  ├── mqtt_subscriber.py (Daemon thread)
  ├── alert_service.py   (WHO/BIS Rule-based WQI Engine)
  ├── database.py        (SQLAlchemy ORM)
  └── app.py             (REST APIs + Static Web Server)
                   │
                   ▼
     [SQLite Database: tds_data.db]
                   │
                   ▼
  [Responsive Frontend Dashboard: localhost:5000]
  ├── 6 Precision Speedometer & Dial Meters
  ├── Overall WQI Scoreboard & Verdict Chip
  ├── Interactive Chart.js Waveform Analyzer
  ├── Contamination Log Table & Toast Notifications
  └── 1-Click CSV Audit File Streaming
```

---

## 7. Water Quality Standards (WHO & BIS IS 10500:2012)

Threshold logic in `alert_service.py` adheres strictly to standard public health recommendations:

| Parameter | Unit | Excellent (Pure) | Safe (Potable) | Warning (Elevated) | Unsafe (Contaminated) |
|---|---|---|---|---|---|
| **TDS** | ppm | $\le 300$ | $300 - 500$ | $500 - 900$ | $> 900$ |
| **pH** | scale | $6.8 - 7.8$ | $6.5 - 8.5$ | $6.0 - 6.5$ / $8.5 - 9.0$ | $< 6.0$ or $> 9.0$ |
| **Turbidity** | NTU | $\le 1.0$ | $1.0 - 5.0$ | $5.0 - 10.0$ | $> 10.0$ |
| **Dissolved Oxygen** | mg/L | $\ge 6.5$ | $5.0 - 6.5$ | $4.0 - 5.0$ | $< 4.0$ |
| **Conductivity (EC)** | µS/cm | $\le 400$ | $400 - 800$ | $800 - 1500$ | $> 1500$ |
| **Temperature** | °C | $18 - 26$ | $15 - 32$ | $32 - 38$ | $> 38$ or $< 10$ |
| **Overall WQI** | $0-100$ | $85 - 100$ | $70 - 84$ | $50 - 69$ | $< 50$ |

---

## 8. Step-by-Step Installation & Execution Guide

### Step 1: Clone Repository
```bash
git clone https://github.com/kxbir-git/WQMS-Real-Time-System.git
cd WQMS-Real-Time-System
```

### Step 2: Install Python Dependencies
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Flash ESP32 Firmware
1. Open `hardware/tds_sensor.ino` in the **Arduino IDE**.
2. Install required libraries (**Sketch → Include Library → Manage Libraries**):
   - `PubSubClient` by Nick O'Leary
   - `OneWire` by Paul Stoffregen
   - `DallasTemperature` by Miles Burton
3. Configure your Wi-Fi SSID and Computer IP:
   ```cpp
   const char* WIFI_SSID     = "Your_WiFi_Hotspot";
   const char* WIFI_PASSWORD = "Your_Password";
   const char* MQTT_BROKER   = "192.168.x.x";  // Computer IP
   ```
4. Select board **ESP32 Dev Module**, choose COM Port, and click **Upload**.

### Step 4: Start Backend Application
```bash
cd backend
python app.py
```
*Console output:*
```text
==================================================
 AquaSense WQMS — Live Hardware Mode Active
 URL: http://localhost:5000
 Waiting for real ESP32 hardware packets...
==================================================
```

### Step 5: Launch Dashboard
Open any browser and navigate to:
```
http://localhost:5000
```
- **Standby Mode**: While ESP32 is powered off, status shows red `"Hardware Disconnected"` and needles rest at $-110^\circ$.
- **Live Activation**: The moment ESP32 powers on and transmits, status turns pulsing green `"Hardware Connected (ESP32)"` and all 6 needles smoothly swing to live sensor measurements!

---

## 9. Live Examination Demonstration Protocol

Prepare 3 test water samples to showcase real-time responsiveness to evaluators:

| Sample | Water Source | Expected Reading | System Reaction |
|---|---|---|---|
| **Sample A** | Commercial RO / Mineral Water | TDS: 90–140 ppm, pH: 7.2, Turb: 0.8 NTU | Meters in **Green Zone**; WQI: ~92; Potability: *"Safe for Drinking"*. |
| **Sample B** | Municipal Tap Water | TDS: 320–420 ppm, pH: 7.6, Turb: 2.1 NTU | Meters in **Blue Zone**; WQI: ~78; Potability: *"Safe / Permissible"*. |
| **Sample C** | Tap Water + 1 pinch Salt & Soil | TDS: >950 ppm, pH: 9.1, Turb: 15.0 NTU | Needle swings to **Red Alert Zone**; WQI: <45; Red Toast Alert pops up; Contamination recorded in Table. |

---

## 10. Repository Structure

```text
WQMS-Real-Time-System/
├── hardware/
│   └── tds_sensor.ino          # ESP32 C++ firmware with median filter & MQTT/HTTP
├── backend/
│   ├── app.py                  # Flask REST API server & static asset host
│   ├── mqtt_subscriber.py      # Background MQTT listener daemon
│   ├── database.py             # SQLAlchemy ORM models (WaterQualityReading)
│   ├── alert_service.py        # Rule-based threshold evaluation & WQI engine
│   ├── config.py               # Configuration constants (ports, limits)
│   ├── requirements.txt        # Python dependency manifest
│   ├── .env.example            # Environment variables template
│   └── mock_sensor.py          # Standalone simulation tool with auto HTTP fallback
├── frontend/
│   ├── index.html              # Responsive dashboard with 6 precision SVG meters
│   ├── style.css               # Light white design system & smooth needle transitions
│   └── script.js               # Gauge animation, live polling & Chart.js waveform logic
├── database/
│   └── .gitkeep                # SQLite database directory (tds_data.db auto-created)
├── .gitignore                  # Git exclusions for python cache & local db
└── README.md                   # Full academic capstone project documentation
```

---

## 11. Academic References

1. **World Health Organization (WHO)**: *Guidelines for Drinking-water Quality (4th Edition)*, Geneva, 2017.
2. **Bureau of Indian Standards (BIS)**: *Indian Standard Drinking Water Specification (Second Revision) IS 10500:2012*.
3. **DFRobot**: *Gravity: Analog TDS Sensor / Meter for Arduino (SEN0244)*.
4. **Espressif Systems**: *ESP32 Technical Reference Manual (ADC & Wi-Fi specifications)*.

---

## 12. License

Distributed under the **MIT License**. Free for academic, educational, and research use.

---

## 13. Complete Deliverables Checklist

| Category | Component / Feature | Deployment Platform / Status | Live Link / Resource |
|---|---|---|---|
| **Frontend UI** | Responsive Real-Time Glassmorphism Console | ✅ **Live & Active** | [https://wqms-sys.vercel.app/](https://wqms-sys.vercel.app/) |
| **Backend API** | Python 3.10 Flask REST Engine (Gunicorn WSGI) | ✅ **Live & Active** | [https://wqms-iot-dashboard.onrender.com](https://wqms-iot-dashboard.onrender.com) |
| **Database** | Telemetry Persistence & Archival | ✅ **Live & Active** | SQLite + SQLAlchemy ORM (`database/water_quality.db`) |
| **Sensors** | 6 Visual Analog Gauges (220° Sweep) | ✅ **Live & Active** | TDS, pH, Turbidity, DO, EC, Temp |
| **Analytics** | Water Quality Index (WQI) Engine | ✅ **Live & Active** | Weighted Arithmetic Index (WHO & BIS IS 10500 compliant) |
| **Waveform** | Interactive Historical Multi-Series Chart | ✅ **Live & Active** | Chart.js 4.4 (24H, 7D, 30D switchable ranges) |
| **Alerts** | Contamination Breach Logging | ✅ **Live & Active** | Real-time visual toasts & threshold deviation panel |
| **Reporting** | Official Inspection Certificate & CSV | ✅ **Live & Active** | Instant CSV download + Printable PDF Inspection Report |
| **Mobile Access** | Cross-Device QR Scanner Modal | ✅ **Live & Active** | Zero-install mobile access via on-screen QR Code |
| **Simulation** | Standalone Hardware Simulator | ✅ **Complete** | `python backend/mock_sensor.py` (Streams directly to cloud) |
| **Firmware** | ESP32 C++ Microcontroller Code | ✅ **Complete** | `hardware/tds_sensor.ino` (12-bit ADC + WiFi + JSON) |
| **Defense** | Viva Guide & Examiner Q&A | ✅ **Complete** | [`docs/VIVA_PREPARATION_AND_PROJECT_DEFENSE.md`](docs/VIVA_PREPARATION_AND_PROJECT_DEFENSE.md) |

