# 🎓 AquaSense WQMS — 24-Slide Presentation Master Deck & 4-Month Project Plan (300 Marks)

> **Project Title:** IoT-Based Real-Time Multi-Parameter Water Quality Monitoring System  
> **Presentation Duration:** 20–25 Minutes (B.Tech Final Year Evaluation — 300 Marks)  
> **Team Structure:** 3 Core Engineering Members + Joint Hardware Fabrication  
> **Development Lifecycle:** 4-Month Academic Capstone Framework (Month 1 to Month 4)  
> **Live Links:** [Frontend Console](https://wqms-sys.vercel.app/) | [Cloud Backend API](https://wqms-iot-dashboard.onrender.com)  

---

## 📅 4-Month Academic Development Framework (Timeline)

```text
========================================================================================
                          4-MONTH DEVELOPMENT WORKFLOW
========================================================================================
 MONTH 1: Research, Feasibility & Hardware Circuit Architecture
   • Literature survey on WHO & BIS IS 10500:2012 drinking water standards.
   • Sensor BOM selection & procurement (ESP32, TDS, pH, Turbidity, DS18B20).
   • ESP32 ADC1 channel allocation & breadboard power rail circuit design.

 MONTH 2: Embedded Firmware, Signal Filtering & Backend Engine
   • C++ firmware development in Arduino framework (`tds_sensor.ino`).
   • 40-sample bubble-sort median filter for analog noise suppression.
   • Flask RESTful API server (`app.py`) & SQLAlchemy ORM database creation.
   • Dual telemetry transport: MQTT broker setup & HTTP direct ingestion fallback.

 MONTH 3: Glassmorphism UI Console, SVG Speedometers & WQI Engine
   • Responsive Single-Page UI in Vanilla HTML5 & Modern CSS3 (`style.css`).
   • 6 Custom SVG analog speedometers with 220° sweep & cubic-bezier easing.
   • Algorithmic Weighted Water Quality Index (WQI) computation (`alert_service.py`).
   • Chart.js interactive historical waveforms, mobile QR code & PDF report generator.

 MONTH 4: Cloud Deployment, 3-Sample Testing & Final Defense
   • Production deployment on Render.com (Gunicorn WSGI) & Vercel Edge CDN.
   • 12-second hardware watchdog integration for live/standby state detection.
   • Physical probe holder fabrication & 3-buffer sensor calibration (pH & TDS).
   • 3-sample lab validation (RO, Municipal Tap, Contaminated Saline Water).
========================================================================================
```

---

## 👥 3-Member Role & Responsibility Distribution

| Member | Role | Core Deliverables |
|---|---|---|
| **Member 1: Naila Javed** | Frontend UI/UX & AI/ML Analytics Lead | Glassmorphism Dashboard, 6 SVG Speedometer Needles, Weighted WQI Engine, Chart.js Waveforms, Mobile QR Modal & PDF Report. |
| **Member 2: Aparna Pandey** | IoT & Sensors Embedded Systems Lead | Sensor Interfacing (TDS, pH, Turbidity, Temp), ESP32 ADC1 Pin Mapping, C++ Firmware, 40-Sample Median Noise Filter, Temperature Compensation. |
| **Member 3: [Your Name]** | Backend, Database & Cloud Deployment Lead | Flask RESTful Ingestion APIs, SQLAlchemy ORM with SQLite, Dual Transport (MQTT + HTTP), Render Cloud & Vercel Reverse Proxy, Hardware Watchdog. |
| **Entire Team** | Hardware Fabrication & Validation (Joint) | Breadboard Circuit Assembly, Probe Waterproof Isolation, 3-Buffer Calibration, 3-Sample Testing Protocol & Presentation Defense. |

---

# 🖥️ 24-Slide Complete PPT Master Deck

---

### Slide 1: Title Slide
* **Title:** AquaSense WQMS — IoT-Based Real-Time Multi-Parameter Water Quality Monitoring System
* **Subtitle:** Final Year B.Tech Computer Science & Engineering Capstone Project (300 Marks)
* **Team Members & Roles:**
  * **Naila Javed** — Frontend Engineering & AI/ML Analytics Lead
  * **Aparna Pandey** — IoT Embedded Systems & Sensors Lead
  * **[Nashra Khan]** — Backend, Database & Cloud Deployment Lead
  * *Joint Effort:* Complete Hardware Rig Assembly, Calibration & Testing
* **Live System URLs:**
  * Live Web App: `https://wqms-sys.vercel.app/`
  * Cloud API: `https://wqms-iot-dashboard.onrender.com`
* **Speaker Notes:**
  > *"Respected external examiners and faculty members, Good Morning. Today we are presenting our final year capstone project: **AquaSense WQMS** — an industrial-grade cyber-physical IoT system that monitors 6 critical drinking water parameters in real time and classifies water health using standard WHO and BIS benchmarks."*

---

### Slide 2: Problem Statement & Industrial Motivation
* **Key Challenges:**
  * **Time Lag:** Conventional laboratory testing requires 24 to 48 hours for titration and incubation reports.
  * **Public Health Risk:** Contaminated water enters consumer distribution lines before lab results arrive.
  * **Lack of Continuous Visibility:** Intermittent manual grab-sampling fails to catch sudden contamination spikes.
  * **High Recurring Cost:** Certified commercial lab testing costs ₹1,500 – ₹3,000 per sample.
* **Our Target:** An automated, in-situ system delivering real-time telemetry every 4 seconds at minimal cost.
* **Speaker Notes:**
  > *"Traditional water quality monitoring relies on physical collection and delayed lab testing. By the time water is declared unsafe, citizens have already consumed it. Our system solves this latency problem by detecting contamination within 4 seconds directly at the source."*

---

### Slide 3: Proposed Solution & Key Objectives
* **Solution Highlights:**
  * Autonomous IoT sensing node measuring **6 physicochemical parameters** simultaneously.
  * On-chip signal conditioning on **ESP32** with 40-sample noise filtering.
  * Deterministic **Water Quality Index (WQI)** computation mapped to public health standards.
  * Dual-cloud deployment with zero-delay browser visualization and instant anomaly alerting.
  * Zero-install cross-device access via on-screen mobile QR scanner.
* **Speaker Notes:**
  > *"Our solution is built on three layers: hardware sensing at the edge, reliable ingestion at the cloud backend, and rich visualization on a modern web dashboard. We have validated our prototype against Indian Standard IS 10500:2012."*

---

### Slide 4: System Architecture (3-Tier Structure)
* **Visual Reference:** `docs/screenshots/system_architecture.svg`
* **3 Functional Layers:**
  1. **Perception Layer:** 4 physical sensors + 2 derived metrics connected to ESP32 DevKit V1.
  2. **Transport & Backend Layer:** Wi-Fi telemetry over HTTP REST / MQTT to Python Flask on Render.
  3. **Presentation Layer:** Glassmorphism UI on Vercel with 6 SVG gauges and Chart.js waveforms.
* **Speaker Notes:**
  > *"The architecture follows a modular 3-tier pattern: the Perception Layer samples raw signals and suppresses noise; the Backend Layer persists data and computes WQI; and the Presentation Layer provides interactive live telemetry."*

---

### Slide 5: Water Quality Standards (WHO & BIS IS 10500:2012)
* **Standard Threshold Reference Matrix:**

| Parameter | Unit | Excellent (Pure) | Safe (Potable) | Unsafe Limit |
|---|---|---|---|---|
| **TDS** | ppm | $\le 300$ | $300 - 500$ | $> 900$ |
| **pH Balance** | pH units | $6.8 - 7.8$ | $6.5 - 8.5$ | $< 6.0$ or $> 9.0$ |
| **Turbidity** | NTU | $\le 1.0$ | $1.0 - 5.0$ | $> 10.0$ |
| **Temperature** | °C | $18 - 25$ | $15 - 32$ | $> 38$ |
| **Dissolved Oxygen** | mg/L | $\ge 6.5$ | $5.0 - 6.5$ | $< 4.0$ |
| **Conductivity** | µS/cm | $\le 400$ | $400 - 800$ | $> 1500$ |

* **Speaker Notes:**
  > *"Our threshold logic is strictly benchmarked against BIS IS 10500:2012 and WHO guidelines. For instance, TDS up to 500 ppm is potable, but anything exceeding 900 ppm triggers an immediate critical alert."*

---

### Slide 6: 4-Month Development Roadmap & Milestones
* **Phase Breakdown:**
  * **Month 1:** Literature survey, WHO/BIS standards review, sensor procurement & pinout design.
  * **Month 2:** C++ firmware development, 40-sample median filter, Flask API & SQLite database setup.
  * **Month 3:** Glassmorphism dashboard, 6 custom SVG speedometers, WQI calculation & Chart.js graphs.
  * **Month 4:** Cloud deployment (Render + Vercel), sensor calibration, 3-sample testing & documentation.
* **Speaker Notes:**
  > *"The project was executed across a 4-month academic schedule. We progressed systematically from requirement analysis in Month 1, to embedded firmware and backend in Month 2, frontend UI and WQI analytics in Month 3, and cloud deployment with physical lab validation in Month 4."*

---

### [SECTION 2: IoT & SENSORS IMPLEMENTATION — Presented by Aparna Pandey]

---

### Slide 7: Hardware Bill of Materials (BOM) & Sensor Selection
* **Presenter:** **Aparna Pandey**
* **Sensors & Microcontroller:**
  * **ESP32 DevKit V1:** 240MHz dual-core Xtensa MCU with integrated 2.4GHz Wi-Fi and 12-bit ADC.
  * **TDS Probe (SEN0244):** Platinum electrodes measuring total dissolved ionic concentration.
  * **pH Glass Probe (E-201-C):** Hydrogen ion potential measurement with BNC signal amplifier.
  * **Turbidity Sensor (SEN0189):** Optical infrared transmittance module measuring suspended cloudiness.
  * **Temperature Sensor (DS18B20):** Waterproof 1-Wire digital probe for thermal tracking.
  * **Total BOM Cost:** Optimized under **₹3,100** for commercial viability.
* **Speaker Notes (Aparna):**
  > *"Good morning teachers. I am Aparna Pandey, responsible for the IoT hardware and perception layer. We selected the ESP32 for its high processing speed, built-in Wi-Fi, and 12-bit ADC resolution, keeping the total BOM cost under ₹3,100."*

---

### Slide 8: Circuit Pinout & ADC1 Channel Allocation
* **Presenter:** **Aparna Pandey**
* **Visual Reference:** `docs/screenshots/hardware_wiring_guide.jpg`
* **Pin Allocation Table:**
  * TDS Sensor (Analog) $\rightarrow$ **GPIO 34** (ADC1_CH6)
  * pH Sensor (Analog) $\rightarrow$ **GPIO 35** (ADC1_CH7)
  * Turbidity Sensor (Analog) $\rightarrow$ **GPIO 32** (ADC1_CH4)
  * DS18B20 Temp (Digital) $\rightarrow$ **GPIO 4** (1-Wire bus with 4.7kΩ pull-up resistor)
* **Critical Design Choice:** All analog sensors are wired strictly to **ADC1** channels. ADC2 channels were avoided because ADC2 is shared with Wi-Fi power amplifiers and shuts down during transmission.
* **Speaker Notes (Aparna):**
  > *"A critical engineering decision was routing all analog sensors strictly to ADC1 channels. On the ESP32, ADC2 cannot sample analog voltages while Wi-Fi is actively transmitting. Our wiring ensures uninterrupted sensor reading during cloud communication."*

---

### Slide 9: Embedded C++ Firmware & Telemetry Dispatch
* **Presenter:** **Aparna Pandey**
* **Firmware Highlights (`hardware/tds_sensor.ino`):**
  * Developed using Arduino ESP32 framework with `PubSubClient`, `OneWire`, and `DallasTemperature`.
  * Configures 12-bit ADC resolution (0–4095 levels) with 11dB input attenuation.
  * Periodically samples sensors every 4,000 milliseconds (4 seconds).
  * Serializes readings into a structured JSON telemetry payload and dispatches via Wi-Fi.
* **Speaker Notes (Aparna):**
  > *"The C++ firmware runs on the ESP32, initializing 12-bit ADC channels and executing sampling every 4 seconds. It normalizes analog signals and compiles a compact JSON packet for cloud transmission."*

---

### Slide 10: 40-Sample Median Filtering Algorithm
* **Presenter:** **Aparna Pandey**
* **The Noise Problem:** Water-immersed probes suffer from stray 50Hz AC hum and switching electrical noise.
* **The Algorithmic Solution:**
  1. Capture 40 consecutive analog samples at 8ms intervals.
  2. Perform an in-place bubble-sort to arrange samples ascendingly.
  3. Discard the top 10 and bottom 10 extreme outliers (voltage spikes and drops).
  4. Average the central 20 values to obtain a steady, clean voltage:
     $$V_{\text{clean}} = \frac{1}{20} \sum_{i=10}^{29} S_{\text{sorted}}[i] \times \frac{3.3}{4096}$$
* **Speaker Notes (Aparna):**
  > *"To eliminate noise without bulky physical filter circuits, I implemented a 40-sample bubble-sort median filter directly in the firmware. Discarding the top and bottom 25% outlier samples gives us laboratory-grade steady readings."*

---

### Slide 11: Temperature Compensation & Calibration
* **Presenter:** **Aparna Pandey**
* **Thermal Compensation Principle:** Water conductivity increases by $\approx 2\%$ per $1^\circ\text{C}$ temperature rise due to increased ion mobility.
* **Normalization Formula (Normalized to 25°C):**
  $$V_{25^\circ\text{C}} = \frac{V_T}{1.0 + 0.02 \times (T - 25.0)}$$
  $$\text{TDS (ppm)} = \left( 133.42 \times V_{25}^3 - 255.86 \times V_{25}^2 + 857.39 \times V_{25} \right) \times 0.5$$
* **pH Calibration:** Calibrated via the Nernst slope equation using pH 7.0 neutral buffer solution.
* **Speaker Notes (Aparna):**
  > *"Because water conductivity increases with temperature, warm water can register as artificially dirty. We normalize all TDS readings to a 25°C baseline using live data from the DS18B20 probe to guarantee true water purity measurements."*

---

### [SECTION 3: BACKEND, DATABASE & CLOUD — Presented by Member 3]

---

### Slide 12: Backend Architecture & RESTful Ingestion Engine
* **Presenter:** **[Nashra Khan]**
* **Backend Stack:** Python 3.10 + Flask + Gunicorn WSGI.
* **Core REST Endpoints:**
  * `POST /api/sensor/data` $\rightarrow$ Ingests JSON telemetry from ESP32.
  * `GET /api/latest` $\rightarrow$ Returns the latest reading with hardware heartbeat check.
  * `GET /api/history` $\rightarrow$ Historical telemetry for Chart.js waveform rendering.
  * `GET /api/stats` $\rightarrow$ Real-time daily Min, Max, and Average summary.
  * `GET /api/export/csv` $\rightarrow$ Streams entire historical database as a timestamped CSV.
* **Speaker Notes (Member 3):**
  > *"Respected teachers, I am [Nashra Khan], responsible for the backend, database, and cloud deployment. I built a Python Flask REST API served by Gunicorn WSGI. It handles telemetry ingestion, database storage, and serves filtered data to the web client."*

---

### Slide 13: Database Design & SQLAlchemy ORM
* **Presenter:** **[Nashra Khan]**
* **Database Architecture (`database.py`):**
  * Uses **SQLAlchemy ORM** mapped to an ACID-compliant **SQLite** database.
  * Stores: `device_id`, `tds_value`, `ph_value`, `turbidity`, `temperature`, `do_value`, `ec_value`, `wqi_value`, `status`, and UTC `timestamp`.
* **Why SQLite + SQLAlchemy?**
  * Zero-configuration, serverless, and low memory footprint (<500KB RAM) for edge deployment.
  * The ORM layer abstracts the database; migrating to PostgreSQL in enterprise mode requires modifying only a single connection string.
* **Speaker Notes (Member 3):**
  > *"We used SQLAlchemy ORM with SQLite for zero-configuration, lightweight persistence. The ORM design ensures that migrating to MySQL or PostgreSQL in an enterprise production environment requires updating only one configuration variable."*

---

### Slide 14: Dual-Transport Communication (MQTT + HTTP Fallback)
* **Presenter:** **[Nashra Khan]**
* **Protocol Comparison:**
  * **Primary Transport (MQTT 3.1.1):** Pub/sub over port 1883 with a 2-byte binary header; minimizes cellular/Wi-Fi bandwidth and battery draw. Handled by a background listener thread (`mqtt_subscriber.py`).
  * **Failover Transport (HTTP REST POST):** Standard JSON POST to `/api/sensor/data`.
* **Reliability Mechanism:** If the local MQTT broker is unreachable or network ports are blocked, the firmware automatically falls back to HTTP POST to ensure zero data loss.
* **Speaker Notes (Member 3):**
  > *"To ensure high availability in remote fields, we implemented dual transport. The ESP32 first attempts lightweight MQTT communication, and if the broker is unavailable, it automatically falls back to standard HTTP POST."*

---

### Slide 15: Cloud Deployment on Render & Vercel
* **Presenter:** **[Nashra Khan]**
* **Deployment Architecture:**
  * **Backend on Render.com:** Containerized Linux web service executing `gunicorn app:app` with automated CI/CD continuous deployment from GitHub.
  * **Frontend on Vercel:** Hosted on Vercel's global Edge Network for sub-50ms static delivery.
* **Cross-Origin Security (CORS):** Solved via `flask-cors` headers on the server and a reverse-proxy rewrite rule in `vercel.json` (`/api/:path*` $\rightarrow$ Render backend), keeping all client requests on the same origin domain.
* **Speaker Notes (Member 3):**
  > *"Both frontend and backend are deployed live on cloud infrastructure. We eliminated browser CORS security issues by setting up a reverse proxy on Vercel that forwards API requests directly to our Render backend."*

---

### Slide 16: Hardware Watchdog & Fail-Safe Telemetry
* **Presenter:** **[Nashra Khan]**
* **The Stale Data Problem:** If the IoT hardware is turned off or loses power, displaying old data as "live" is dangerously misleading.
* **The 12-Second Watchdog Mechanism:**
  * The backend computes reading age: $\Delta t = \text{CurrentTime} - \text{LatestTimestamp}$.
  * If $\Delta t \le 12.0\text{s}$ $\rightarrow$ Status: **"Hardware Connected (ESP32)"** (Pulsing Green).
  * If $\Delta t > 12.0\text{s}$ $\rightarrow$ Status: **"Hardware Disconnected"** (Red Alert); dashboard needles smoothly drop to the standby position ($-110^\circ$).
* **Speaker Notes (Member 3):**
  > *"We built an automated 12-second watchdog timer. If the ESP32 is powered off or disconnected, the backend flags the stream as inactive, and the dashboard immediately informs the user that hardware is disconnected rather than showing stale data."*

---

### [SECTION 4: FRONTEND UI/UX & AI/ML — Presented by Naila Javed]

---

### Slide 17: Frontend Architecture & Glassmorphism UI
* **Presenter:** **Naila Javed**
* **Visual Reference:** `docs/screenshots/dashboard_live.png`
* **UI/UX Design Philosophy:**
  * Modern, light-white design system (`#FFFFFF` cards, `#F7F9FC` canvas, `#2E86DE` ocean accents).
  * Glassmorphism aesthetics with CSS backdrop filters (`backdrop-filter: blur(16px)`).
  * Built using pure Vanilla HTML5, Modern CSS3, and ES6+ JavaScript.
  * Zero bulky frameworks (no React/Angular overhead), achieving instant page load under 350ms.
* **Speaker Notes (Naila):**
  > *"Good morning teachers. I am Naila Javed, and I led the frontend engineering and AI/ML analytics. We built a clean, executive glassmorphism dashboard using pure vanilla HTML5 and CSS3, achieving sub-350ms loading times without framework bloat."*

---

### Slide 18: Custom SVG Speedometers & 220° Dial Gauges
* **Presenter:** **Naila Javed**
* **Engineering Precision SVG Meters:**
  * 6 dedicated analog meters for all 6 water quality parameters.
  * Calibrated 220° circular sweep arc from $-110^\circ$ to $+110^\circ$.
* **Needle Angle Formula:**
  $$\theta = -110^\circ + \left( \frac{\text{Value} - \text{Min}}{\text{Max} - \text{Min}} \right) \times 220^\circ$$
* **Physical Inertia:** Needle transitions are animated using a custom CSS easing curve:
  `cubic-bezier(0.22, 1, 0.36, 1)` for realistic mechanical movement.
* **Speaker Notes (Naila):**
  > *"Instead of using third-party chart libraries for meters, I coded all 6 speedometers from scratch in pure SVG. Using linear trigonometric scaling and cubic-bezier easing, the needles rotate with natural physical inertia as sensor values update."*

---

### Slide 19: AI/ML Analytics & Weighted WQI Engine
* **Presenter:** **Naila Javed**
* **Why WQI?** Raw numbers alone do not tell citizens whether water is safe to drink.
* **Weighted Arithmetic Index Formula:**
  $$\text{WQI} = \frac{\sum (W_i \times q_i)}{\sum W_i}$$
  * $W_i$: Unit weight inversely proportional to permissible standard limit ($S_i$).
  * $q_i$: Quality rating sub-index normalized against ideal values.
* **Predictive Classification:**
  * **90–100:** *Excellent (Pristine / RO Drinkable)*
  * **70–89:** *Good / Safe (Municipal Tap Supply)*
  * **50–69:** *Poor (Requires Active Filtration)*
  * **< 50:** *Unfit / Hazardous (Immediate Alert Triggered)*
* **Speaker Notes (Naila):**
  > *"My core analytical contribution was the multi-parameter WQI Engine. Using the Weighted Arithmetic Index method, our algorithm normalizes all 6 parameters into a single 0-to-100 composite index, automatically classifying potability and identifying the dominant risk factor."*

---

### Slide 20: Interactive Historical Waveforms (Chart.js 4.4)
* **Presenter:** **Naila Javed**
* **Waveform Features:**
  * Canvas-rendered multi-series time-series chart using Chart.js 4.4.
  * Parameter tabs allowing operators to switch between TDS, pH, Turbidity, Temp, DO, and EC.
  * Switchable historical query ranges: 24 Hours, 7 Days, and 30 Days.
  * Smooth Bézier curve interpolation for visual trend clarity.
* **Speaker Notes (Naila):**
  > *"To track temporal changes, I integrated Chart.js waveforms with tab switching across all 6 parameters. Operators can inspect 24-hour, 7-day, or 30-day trends to identify seasonal degradation or pipeline contamination events."*

---

### Slide 21: Mobile QR Integration & Official PDF Certificate
* **Presenter:** **Naila Javed**
* **Visual Reference:** `docs/screenshots/mobile_view.png`
* **Enterprise Usability Features:**
  * **Mobile QR Modal:** An on-screen QR code allows teachers and field inspectors to scan and open the responsive dashboard instantly on their mobile phones with zero app installation.
  * **Official PDF Inspection Certificate:** A dedicated print stylesheet (`@media print`) formats the dashboard into an official, A4 water quality inspection certificate with timestamps and compliance badges.
  * **CSV Audit Export:** One-click streaming download of raw database tables.
* **Speaker Notes (Naila):**
  > *"We added two key features for field use: an on-screen QR code for zero-install mobile access, and a printable A4 inspection certificate that formats live telemetry into an official compliance report with one click."*

---

### [SECTION 5: HARDWARE RIG, TESTING & CONCLUSION — Entire Team]

---

### Slide 22: Hardware Prototyping & Rig Fabrication
* **Presenter:** **Joint Team (All 3 Members)**
* **Collaborative Hardware Work:**
  * Assembled circuit on a 400-point breadboard with distributed 5V and 3.3V power rails.
  * Fabricated an acrylic probe mounting holder to submerge probes stably in the water vessel.
  * Isolated probe grounds and signal cables to prevent capacitive interference.
  * Conducted 3-point calibration using standard pH 4.01, 7.00, and 9.18 buffer solutions.
* **Speaker Notes (Joint):**
  > *"Hardware fabrication was a collaborative effort by all three members. We built the breadboard circuit, isolated sensor grounds to prevent interference, waterproofed the wiring, and calibrated the probes using standard laboratory buffer solutions."*

---

### Slide 23: Live 3-Sample Testing Results
* **Presenter:** **Joint Team**
* **Laboratory Validation Results:**

| Test Sample | Source Water | Measured TDS / pH / Turb | System Reaction & WQI |
|---|---|---|---|
| **Sample A** | Commercial RO / Mineral Water | TDS: 110 ppm, pH: 7.2, Turb: 0.8 NTU | Needles in **Green Zone**; WQI: **92** (*Safe for Drinking*). |
| **Sample B** | Municipal Tap Water | TDS: 380 ppm, pH: 7.6, Turb: 2.2 NTU | Needles in **Blue Zone**; WQI: **78** (*Permissible Supply*). |
| **Sample C** | Tap Water + Pinch of Salt & Soil | TDS: >950 ppm, pH: 9.1, Turb: 14.5 NTU | Needles swing to **Red Alert Zone**; WQI: **42** (*Unfit / Contaminated*). |

* **Speaker Notes (Joint):**
  > *"We validated our prototype using three real-world water samples. Notice how transitioning from pure RO water to contaminated water causes the meters to swing to the red zone within 4 seconds, automatically dropping the WQI below 50 and triggering an alert."*

---

### Slide 24: Conclusion, Future Scope & Project Summary
* **Presenter:** **Joint Team**
* **Project Achievements:**
  * Engineered an operational real-time IoT water monitoring system under ₹3,100 BOM.
  * Sub-4-second edge-to-cloud telemetry with dual-transport reliability (MQTT + HTTP).
  * Built custom 40-sample median filtering, temperature compensation, and WQI analytics.
  * Deployed live cloud dashboard with mobile sync, PDF reporting, and CSV streaming.
* **Future Scope:**
  * Machine learning forecasting using LSTM neural networks for predictive contamination trends.
  * Integration of long-range LoRaWAN for remote rural monitoring up to 10 km.
  * Relay-actuated automated dosing valves for chemical neutralization.
* **Speaker Notes (Joint):**
  > *"In conclusion, AquaSense WQMS proves that automated, standards-compliant water quality monitoring can be achieved reliably and affordably. Thank you, and we are now ready for your questions."*

---

## 💡 Quick Viva Defense Tips for the 3 Members

* **Aparna Pandey:** Be ready to answer questions about the **40-sample median filter**, **ADC1 vs ADC2**, and **temperature compensation formula**.
* **Member 3:** Be ready to explain the **Flask REST API**, **SQLAlchemy ORM**, **MQTT vs HTTP failover**, and **CORS reverse proxy on Vercel**.
* **Naila Javed:** Be ready to explain the **WQI Weighted Arithmetic formula**, **SVG speedometer needle mathematics**, and **Chart.js waveform logic**.
