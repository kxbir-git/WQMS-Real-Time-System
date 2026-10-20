"""
generate_ppt.py — Generates a professional 24-slide widescreen PowerPoint presentation (.pptx)
for AquaSense WQMS Capstone Defense (300 Marks).
Includes embedded screenshots, 3-member distribution, 4-month academic timeline,
and footer with Date, Time, and Slide Numbers.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(15, 30, 65)         # Deep Navy Blue
    C_OCEAN = RGBColor(14, 116, 144)      # Ocean Cyan / Teal
    C_LIGHT_BG = RGBColor(248, 250, 252)  # Soft background
    C_CARD_BG = RGBColor(255, 255, 255)   # White card
    C_BORDER = RGBColor(226, 232, 240)    # Soft slate border
    C_TEXT_DARK = RGBColor(15, 23, 42)    # Slate 900
    C_TEXT_MUTED = RGBColor(71, 85, 105)  # Slate 600
    C_WHITE = RGBColor(255, 255, 255)
    C_PILL_BG = RGBColor(224, 242, 254)   # Sky 100
    C_PILL_TXT = RGBColor(3, 105, 161)    # Sky 700

    IMG_DASHBOARD = os.path.abspath("docs/screenshots/dashboard_live.png")
    IMG_HARDWARE = os.path.abspath("docs/screenshots/hardware_wiring_guide.jpg")
    IMG_MOBILE = os.path.abspath("docs/screenshots/mobile_view.png")

    def add_header_and_footer(slide, title, section_name, presenter_name, slide_num, total_slides=24):
        # Top banner background strip
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_NAVY
        top_bar.line.fill.background()

        # Accent thin line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = C_OCEAN
        line.line.fill.background()

        # Section tag & Title box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(8.5), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = section_name.upper()
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(125, 211, 252)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE

        # Presenter Badge Box (Right side)
        pb = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(0.35), Inches(3.0), Inches(0.5))
        pb.fill.solid()
        pb.fill.fore_color.rgb = RGBColor(30, 58, 110)
        pb.line.color.rgb = RGBColor(56, 189, 248)
        pbtf = pb.text_frame
        pbtf.word_wrap = True
        pbtf.margin_left = pbtf.margin_top = pbtf.margin_right = pbtf.margin_bottom = 0
        pbp = pbtf.paragraphs[0]
        pbp.text = f"👤 {presenter_name}"
        pbp.font.size = Pt(11)
        pbp.font.bold = True
        pbp.font.color.rgb = RGBColor(224, 242, 254)
        pbp.alignment = PP_ALIGN.CENTER

        # Bottom Footer Bar
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.05), Inches(13.333), Inches(0.45))
        footer.fill.solid()
        footer.fill.fore_color.rgb = C_NAVY
        footer.line.fill.background()

        # Footer Text Box
        ftb = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(11.733), Inches(0.35))
        ftf = ftb.text_frame
        ftf.word_wrap = True
        ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0

        fp = ftf.paragraphs[0]
        fp.text = f"AquaSense WQMS — IoT Capstone Defense (300 Marks)   |   Date: October 20, 2026  •  Time: 18:15 IST   |   Slide {slide_num} of {total_slides}"
        fp.font.size = Pt(10)
        fp.font.color.rgb = RGBColor(203, 213, 225)
        fp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Joint)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(5.6), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 110)
    pill.line.color.rgb = RGBColor(56, 189, 248)
    ptf = pill.text_frame
    ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
    ptfp = ptf.paragraphs[0]
    ptfp.text = "B.TECH CSE FINAL YEAR CAPSTONE PROJECT DEFENSE (300 MARKS)"
    ptfp.font.size = Pt(9.5)
    ptfp.font.bold = True
    ptfp.font.color.rgb = RGBColor(224, 242, 254)
    ptfp.alignment = PP_ALIGN.CENTER

    # Main Title
    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(1.6))
    t1f = t1.text_frame
    t1f.word_wrap = True
    p = t1f.paragraphs[0]
    p.text = "AquaSense WQMS"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p2 = t1f.add_paragraph()
    p2.text = "IoT-Based Real-Time Multi-Parameter Water Quality Monitoring System"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(56, 189, 248)

    # 3 Member Cards
    members = [
        ("Naila Javed", "Frontend & AI/ML Lead", "Glassmorphism UI, 6 SVG Speedometers, Weighted WQI Engine & Analytics"),
        ("Aparna Pandey", "IoT & Sensors Lead", "ESP32 Firmware, ADC1 Pin Allocation, 40-Sample Median Filter, Calibration"),
        ("Member 3", "Backend & Deployment Lead", "Flask REST API, SQLAlchemy SQLite DB, Render/Vercel Cloud Deploy, Watchdog")
    ]
    card_w = Inches(3.7)
    gap = Inches(0.3)
    start_x = Inches(0.8)

    for i, (m_name, m_role, m_desc) in enumerate(members):
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x + i * (card_w + gap), Inches(3.3), card_w, Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(23, 42, 85)
        card.line.color.rgb = RGBColor(71, 85, 105)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_top = Inches(0.2)
        ctf.margin_left = Inches(0.25)
        ctf.margin_right = Inches(0.25)

        cp1 = ctf.paragraphs[0]
        cp1.text = f"👤 {m_name}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = C_WHITE

        cp2 = ctf.add_paragraph()
        cp2.text = m_role
        cp2.font.size = Pt(11.5)
        cp2.font.bold = True
        cp2.font.color.rgb = RGBColor(56, 189, 248)

        cp3 = ctf.add_paragraph()
        cp3.text = m_desc
        cp3.font.size = Pt(10)
        cp3.font.color.rgb = RGBColor(203, 213, 225)

    # Joint Team Note
    jbox = s1.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.7), Inches(0.8))
    jtf = jbox.text_frame
    jp = jtf.paragraphs[0]
    jp.text = "🤝 Joint Hardware Fabrication: Complete Breadboard Circuit Assembly, Probe Isolation, 3-Buffer Calibration & Lab Testing by Entire Team"
    jp.font.size = Pt(11)
    jp.font.color.rgb = RGBColor(148, 163, 184)
    jp.alignment = PP_ALIGN.CENTER

    # Footer on slide 1
    f1 = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.5))
    f1tf = f1.text_frame
    f1p = f1tf.paragraphs[0]
    f1p.text = "Live Web App: https://wqms-sys.vercel.app/   |   Cloud API: https://wqms-iot-dashboard.onrender.com   |   Date: October 20, 2026"
    f1p.font.size = Pt(10)
    f1p.font.color.rgb = RGBColor(148, 163, 184)
    f1p.alignment = PP_ALIGN.CENTER

    # Helper function for regular content slides
    def add_content_slide(slide_num, title, section, presenter, left_title, left_bullets, right_title, right_bullets, img_path=None):
        slide = prs.slides.add_slide(blank_layout)
        add_header_and_footer(slide, title, section, presenter, slide_num)

        # Left Column Card
        col_w = Inches(5.6) if not img_path else Inches(6.2)
        c1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w, Inches(5.2))
        c1.fill.solid()
        c1.fill.fore_color.rgb = C_CARD_BG
        c1.line.color.rgb = C_BORDER
        c1_tf = c1.text_frame
        c1_tf.word_wrap = True
        c1_tf.margin_left = c1_tf.margin_right = c1_tf.margin_top = Inches(0.3)

        p = c1_tf.paragraphs[0]
        p.text = left_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_NAVY

        for b in left_bullets:
            bp = c1_tf.add_paragraph()
            bp.text = f"•  {b}"
            bp.font.size = Pt(12)
            bp.font.color.rgb = C_TEXT_DARK
            bp.space_before = Pt(8)

        # Right Column (Either Image or Second Card)
        if img_path and os.path.exists(img_path):
            # Add image in right area
            img_x = Inches(7.3)
            img_y = Inches(1.5)
            img_w = Inches(5.2)
            slide.shapes.add_picture(img_path, img_x, img_y, width=img_w)
            
            # Caption under image
            cap_box = slide.shapes.add_textbox(img_x, Inches(6.3), img_w, Inches(0.5))
            ctf = cap_box.text_frame
            cp = ctf.paragraphs[0]
            cp.text = right_title
            cp.font.size = Pt(11)
            cp.font.italic = True
            cp.font.color.rgb = C_TEXT_MUTED
            cp.alignment = PP_ALIGN.CENTER
        else:
            c2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
            c2.fill.solid()
            c2.fill.fore_color.rgb = C_CARD_BG
            c2.line.color.rgb = C_BORDER
            c2_tf = c2.text_frame
            c2_tf.word_wrap = True
            c2_tf.margin_left = c2_tf.margin_right = c2_tf.margin_top = Inches(0.3)

            p2 = c2_tf.paragraphs[0]
            p2.text = right_title
            p2.font.size = Pt(16)
            p2.font.bold = True
            p2.font.color.rgb = C_NAVY

            for b in right_bullets:
                bp2 = c2_tf.add_paragraph()
                bp2.text = f"•  {b}"
                bp2.font.size = Pt(12)
                bp2.font.color.rgb = C_TEXT_DARK
                bp2.space_before = Pt(8)

        return slide

    # =========================================================================
    # SLIDES 2 to 6: OVERVIEW & STANDARDS
    # =========================================================================
    add_content_slide(
        2, "Problem Statement & Real-World Challenges", "Project Overview", "Entire Team",
        "The Conventional Testing Problem",
        [
            "High Latency: Standard laboratory titration takes 24 to 48 hours for reports.",
            "Health Risks: Contaminated water is consumed before lab results arrive.",
            "Lack of Temporal Visibility: Manual grab-sampling misses intermittent pipe bursts.",
            "Excessive Cost: Commercial laboratory testing costs ₹1,500 – ₹3,000 per sample."
        ],
        "AquaSense Cyber-Physical Target",
        [
            "Autonomous Continuous Monitoring: Live telemetry captured every 4 seconds.",
            "Multi-Parameter Sensing: 6 critical chemical and physical indicators monitored.",
            "Zero Human Delay: Immediate cloud contamination alerts triggered at source.",
            "Cost Efficiency: Prototype fabricated under ₹3,100 with zero recurring costs."
        ]
    )

    add_content_slide(
        3, "Proposed Solution & System Objectives", "Project Overview", "Entire Team",
        "Key Engineering Objectives",
        [
            "In-Situ Sensing: Direct immersion of waterproof probes in distribution vessels.",
            "Hardware Edge Processing: On-chip signal conditioning & 40-sample median filtering.",
            "Dynamic Temperature Compensation: Eliminates thermal drift in conductivity readings.",
            "Deterministic WQI Scoring: Single composite health index (0-100) per WHO & BIS."
        ],
        "Full-Stack System Deliverables",
        [
            "Dual-Transport Telemetry: MQTT broker pipeline with HTTP REST fallback.",
            "Light-Themed Glassmorphism UI: 6 SVG speedometers with physical inertia.",
            "Historical Waveform Analyzer: Multi-series temporal charts via Chart.js 4.4.",
            "Cross-Device Mobility: Zero-install on-screen QR code scanner for field officers."
        ]
    )

    add_content_slide(
        4, "System Architecture & 3-Tier Data Pipeline", "Architecture", "Entire Team",
        "3-Tier Structural Overview",
        [
            "Perception Layer (Edge): ESP32 MCU + 4 physical probes (TDS, pH, Turbidity, Temp).",
            "Transport & Ingestion Layer: JSON payload over Wi-Fi 802.11 b/g/n (MQTT / HTTP REST).",
            "Backend Processing Layer: Python Flask server on Render + SQLite DB (SQLAlchemy ORM).",
            "Presentation Layer (Client): Vercel Edge CDN dashboard with sub-50ms loading."
        ],
        "Live System Architecture",
        [],
        img_path=IMG_DASHBOARD
    )

    add_content_slide(
        5, "Water Quality Standards (WHO & BIS IS 10500:2012)", "Standards & Safety", "Entire Team",
        "Public Health Benchmarks",
        [
            "Total Dissolved Solids (TDS): Ideal ≤ 300 ppm | Safe: 300-500 ppm | Unsafe: > 900 ppm.",
            "pH Balance: Neutral: 6.8 - 7.8 | Safe: 6.5 - 8.5 | Unsafe: < 6.0 or > 9.0.",
            "Turbidity (Cloudiness): Ideal ≤ 1.0 NTU | Safe: 1.0 - 5.0 NTU | Unsafe: > 10.0 NTU.",
            "Temperature: Ambient: 15 - 32 °C | Thermal Warning: > 38 °C."
        ],
        "Secondary Indicators & WQI",
        [
            "Dissolved Oxygen (DO): Ideal ≥ 6.5 mg/L | Safe: 5.0 - 6.5 mg/L | Unsafe: < 4.0 mg/L.",
            "Electrical Conductivity (EC): Ideal ≤ 400 µS/cm | Safe: 400 - 800 µS/cm.",
            "Overall WQI Composite Index: 90-100 (Excellent), 70-89 (Safe), <50 (Unfit for Drinking).",
            "Regulatory Compliance: Formulated strictly per Indian Standard BIS IS 10500:2012."
        ]
    )

    add_content_slide(
        6, "4-Month Academic Development Framework", "Project Planning", "Entire Team",
        "Semester Development Sprints",
        [
            "Month 1: Literature review, WHO/BIS standards mapping, BOM procurement & pinout design.",
            "Month 2: C++ firmware coding, 40-sample median filter, Flask API & SQLite database setup.",
            "Month 3: Glassmorphism UI, 6 SVG speedometers, WQI algorithm & Chart.js waveforms.",
            "Month 4: Cloud deployment (Render + Vercel), 3-buffer calibration & lab sample testing."
        ],
        "Specialized Member Responsibilities",
        [
            "Aparna Pandey: Hardware perception, ESP32 ADC1 wiring, firmware & sensor calibration.",
            "Member 3: Flask REST APIs, SQLAlchemy database, Render deployment & watchdog.",
            "Naila Javed: UI/UX glassmorphism, SVG meters, WQI calculation & mobile QR access.",
            "Entire Team: Physical breadboard wiring, probe isolation & 3-sample validation."
        ]
    )

    # =========================================================================
    # SLIDES 7 to 11: IOT & SENSORS (Aparna Pandey)
    # =========================================================================
    add_content_slide(
        7, "Hardware Bill of Materials (BOM) & Sensor Selection", "IoT & Sensors Layer", "Aparna Pandey",
        "Core Hardware Components",
        [
            "ESP32 DevKit V1: 240MHz dual-core Xtensa MCU with integrated 2.4GHz Wi-Fi and 12-bit ADC.",
            "TDS Sensor (SEN0244): Dual-pin probe measuring dissolved ion conductance (0-1500 ppm).",
            "pH Sensor Probe (E-201-C): Glass electrode with BNC signal amplifier board (0-14 pH).",
            "Optical Turbidity (SEN0189): Infrared emitter/detector measuring suspended scatter.",
            "Digital Temp (DS18B20): Waterproof stainless steel thermal probe with 1-Wire bus."
        ],
        "Hardware Wiring Guide",
        [],
        img_path=IMG_HARDWARE
    )

    add_content_slide(
        8, "ESP32 Pinout & ADC1 Channel Allocation", "IoT & Sensors Layer", "Aparna Pandey",
        "Exact Pin-to-Pin Circuit Mapping",
        [
            "TDS Sensor AOUT → GPIO 34 (ADC1_CH6, Analog Input)",
            "pH Sensor AOUT → GPIO 35 (ADC1_CH7, Analog Input)",
            "Turbidity Sensor AOUT → GPIO 32 (ADC1_CH4, Analog Input)",
            "DS18B20 Data → GPIO 4 (1-Wire Bus with 4.7kΩ pull-up resistor to 3.3V)"
        ],
        "Critical Engineering Decision: ADC1 vs ADC2",
        [
            "ESP32 Architecture Constraint: ADC2 channels are shared with Wi-Fi power circuits.",
            "If analog sensors are wired to ADC2 (GPIO 2, 4, 12-15), readings corrupt during transmission.",
            "All analog sensors were strictly isolated on ADC1 channels (GPIO 32, 34, 35).",
            "Guarantees 100% uninterrupted, noise-free sampling during live Wi-Fi streaming."
        ]
    )

    add_content_slide(
        9, "Embedded C++ Firmware & Sampling Engine", "IoT & Sensors Layer", "Aparna Pandey",
        "Firmware Architecture (`tds_sensor.ino`)",
        [
            "Framework: Arduino C++ with PubSubClient, OneWire, and DallasTemperature libraries.",
            "12-Bit ADC Configuration: analogReadResolution(12) yielding 0–4095 discrete levels.",
            "Analog Attenuation: analogSetAttenuation(ADC_11db) for full 0 to 3.3V dynamic range.",
            "Non-Blocking Timing: Uses millis() timer (4000ms interval) instead of blocking delay()."
        ],
        "Telemetry Payload Dispatch",
        [
            "Serializes cleaned metrics into structured JSON string format.",
            "Payload attributes: device_id, tds, ph, turbidity, temperature, do, ec.",
            "Dispatches packet to local/cloud MQTT broker on topic water/tds/data.",
            "Includes local Serial debugging output for real-time serial terminal audits."
        ]
    )

    add_content_slide(
        10, "40-Sample Median Filtering Algorithm", "IoT & Sensors Layer", "Aparna Pandey",
        "The Analog Noise Problem",
        [
            "Submerged water probes act as miniature antennas, picking up 50Hz electrical hum.",
            "Nearby pump motors and power adapters cause abrupt voltage spikes and dips.",
            "Simple arithmetic averaging fails because severe spikes skew the mean value."
        ],
        "4-Step Median Noise Filter Implementation",
        [
            "Step 1: Capture 40 consecutive raw analog samples spaced at 8ms intervals.",
            "Step 2: Execute an in-place bubble-sort to arrange samples in ascending order.",
            "Step 3: Discard the 10 lowest and 10 highest samples (trimming 50% extreme outliers).",
            "Step 4: Average the central 20 samples to obtain a steady, laboratory-grade baseline voltage."
        ]
    )

    add_content_slide(
        11, "Temperature Compensation & Sensor Calibration", "IoT & Sensors Layer", "Aparna Pandey",
        "Temperature Compensation Principle",
        [
            "Conductivity increases ~2% per 1°C temperature rise due to decreased water viscosity.",
            "Warm water registers artificially high TDS without proper compensation.",
            "Normalization Equation (Normalized to 25°C reference):",
            "V_25C = V_measured / (1.0 + 0.02 * (Temp - 25.0))",
            "TDS (ppm) = (133.42 * V_25^3 - 255.86 * V_25^2 + 857.39 * V_25) * 0.5"
        ],
        "Laboratory Sensor Calibration",
        [
            "pH Sensor Calibration: Submerged in standard pH 7.00 buffer solution; adjusted amplifier pot.",
            "TDS Sensor Calibration: Tested in 1413 µS/cm conductivity reference and distilled water.",
            "Turbidity Calibration: 4.2V represents clear drinking water (0 NTU); <2.5V indicates turbid."
        ]
    )

    # =========================================================================
    # SLIDES 12 to 16: BACKEND & CLOUD (Member 3)
    # =========================================================================
    add_content_slide(
        12, "Backend Architecture & RESTful Ingestion Engine", "Backend & Cloud Layer", "Member 3",
        "Flask REST API Engine (`app.py`)",
        [
            "Python 3.10 microframework with Gunicorn WSGI production web server.",
            "Non-blocking architecture handling multi-client polling and ingestion concurrently.",
            "Thread-Safe Ingestion: Dedicated background workers process incoming sensor telemetry."
        ],
        "Primary REST Endpoints",
        [
            "POST /api/sensor/data — Ingests JSON telemetry from ESP32 or simulation tool.",
            "GET /api/latest — Returns latest telemetry record with hardware watchdog status.",
            "GET /api/history — Historical readings for Chart.js waveform trend visualization.",
            "GET /api/stats — Real-time aggregation of today's Min, Max, and Average metrics.",
            "GET /api/export/csv — Streams the entire database as a downloadable CSV spreadsheet."
        ]
    )

    add_content_slide(
        13, "Database Architecture & SQLAlchemy ORM", "Backend & Cloud Layer", "Member 3",
        "Relational Schema Design (`database.py`)",
        [
            "Table Name: water_readings",
            "Fields: id (Primary Key), device_id, tds_value, ph_value, turbidity, temperature",
            "Derived Metrics: do_value, ec_value, wqi_value, status (Safe/Warning/Unsafe)",
            "Timestamp: UTC DateTime index for accelerated time-series historical queries."
        ],
        "Why SQLite with SQLAlchemy ORM?",
        [
            "Serverless & Lightweight: Negligible memory footprint (<500KB RAM) for edge deployment.",
            "Zero Configuration: Auto-creates tds_data.db without requiring daemon installations.",
            "Enterprise Portability: Using SQLAlchemy ORM allows migrating to PostgreSQL via 1 config URI.",
            "Thread Safety: check_same_thread=False enabled for multi-threaded Flask requests."
        ]
    )

    add_content_slide(
        14, "Dual-Transport Communication (MQTT + HTTP Fallback)", "Backend & Cloud Layer", "Member 3",
        "MQTT Protocol (Primary Ingestion)",
        [
            "Lightweight publish-subscribe architecture running over TCP port 1883.",
            "2-byte binary header minimizes battery drain and cellular/Wi-Fi bandwidth.",
            "Background daemon thread (mqtt_subscriber.py) continuously ingests incoming packets."
        ],
        "HTTP REST Fallback & Fault Tolerance",
        [
            "Direct HTTP Ingestion: ESP32 dispatches POST requests directly to cloud API.",
            "Automated Failover: If MQTT broker is unreachable or blocked, HTTP fallback activates.",
            "Guarantees zero packet loss during field network transitions or firewall blocks."
        ]
    )

    add_content_slide(
        15, "Cloud Deployment on Render & Vercel", "Backend & Cloud Layer", "Member 3",
        "Render.com Backend Container",
        [
            "Containerized Linux web service executing gunicorn app:app --workers 2.",
            "Automated continuous deployment (CI/CD) directly from GitHub repository.",
            "Environment variables managed securely via render.yaml manifest."
        ],
        "Vercel Frontend & CORS Proxy",
        [
            "Static asset deployment on Vercel's global Edge Network (sub-50ms latency).",
            "Cross-Origin (CORS) Solution: Server-side flask-cors combined with vercel.json rewrite.",
            "Reverse Proxy: All /api/* calls are transparently forwarded to Render backend."
        ]
    )

    add_content_slide(
        16, "Hardware Watchdog & Fail-Safe Telemetry", "Backend & Cloud Layer", "Member 3",
        "The Stale Data Problem",
        [
            "In IoT monitoring, presenting outdated data as 'live' when hardware powers off is dangerous.",
            "If an ESP32 loses power or probe disconnects, the user must be alerted immediately."
        ],
        "12-Second Watchdog Mechanism",
        [
            "Backend computes telemetry age: Age = CurrentTime - LatestRecordTimestamp.",
            "Live State (Age ≤ 12.0s): Status displays pulsing green 'Hardware Connected (ESP32)'.",
            "Disconnected State (Age > 12.0s): Status displays red alert 'Hardware Disconnected'.",
            "Safe Standby: Dashboard needles automatically drop to the -110° resting position."
        ]
    )

    # =========================================================================
    # SLIDES 17 to 21: FRONTEND & AI/ML (Naila Javed)
    # =========================================================================
    add_content_slide(
        17, "Frontend Architecture & Glassmorphism Design", "Frontend & AI/ML Layer", "Naila Javed",
        "Design System & Aesthetics",
        [
            "Modern Light Palette: Crisp white cards (#FFFFFF), soft canvas (#F7F9FC), ocean blue (#2E86DE).",
            "Glassmorphism UI: CSS backdrop-filter: blur(16px) with translucent borders.",
            "Pure Vanilla Stack: Built with HTML5, Modern CSS3, and ES6+ JavaScript.",
            "Zero Framework Overhead: Loads instantaneously under 350ms with zero build steps."
        ],
        "Live Dashboard Interface",
        [],
        img_path=IMG_DASHBOARD
    )

    add_content_slide(
        18, "Custom SVG Speedometers & 220° Dial Gauges", "Frontend & AI/ML Layer", "Naila Javed",
        "Mathematical Gauge Geometry",
        [
            "6 Dedicated Analog Meters: TDS, pH Level, Turbidity, Temp, DO, and Conductivity.",
            "Calibrated Sweep: Unified 220° circular arc spanning from -110° to +110°.",
            "Angular Mapping: Theta = -110° + ((Value - Min) / (Max - Min)) * 220°",
            "Trigonometric Tick Placement: Line endpoints calculated dynamically via sine and cosine."
        ],
        "Physical Inertia & Animation",
        [
            "Needles animated via CSS cubic-bezier(0.22, 1, 0.36, 1) easing curve.",
            "Simulates real mechanical inertia, preventing jarring jumps when data updates.",
            "Pure SVG implementation eliminates canvas pixelation on high-DPI retina screens."
        ]
    )

    add_content_slide(
        19, "AI/ML Analytics & Weighted WQI Engine", "Frontend & AI/ML Layer", "Naila Javed",
        "Why Water Quality Index (WQI)?",
        [
            "Raw sensor numbers can confuse end-users who only want to know: 'Is this water safe?'",
            "WQI compresses 6 complex physical and chemical dimensions into a single 0-100 score."
        ],
        "Weighted Arithmetic Formulation",
        [
            "Formula: WQI = Sum(Wi * qi) / Sum(Wi)",
            "Wi (Unit Weight): Inversely proportional to standard permissible limits (Wi = K / Si).",
            "qi (Quality Sub-index): Normalized distance between actual value and ideal standard.",
            "Predictive Potability Verdict: 90-100 (Excellent/Drinkable), 70-89 (Safe), <50 (Unfit)."
        ]
    )

    add_content_slide(
        20, "Interactive Historical Waveforms (Chart.js 4.4)", "Frontend & AI/ML Layer", "Naila Javed",
        "Temporal Trend Visualizer",
        [
            "Canvas-rendered interactive time-series chart integrated via Chart.js 4.4.",
            "Multi-Series Tab Switching: Instant toggle between TDS, pH, Turbidity, Temp, DO, and EC.",
            "Custom Range Selectors: Query database history across 24 Hours, 7 Days, or 30 Days."
        ],
        "Operational Value",
        [
            "Bézier curve interpolation provides clear visibility into daily contamination spikes.",
            "Enables municipal operators to pinpoint contamination timing after heavy rainfall or pipe bursts.",
            "Dynamic tooltip inspection displays exact timestamp and parameter readings on hover."
        ]
    )

    add_content_slide(
        21, "Mobile QR Integration & Official PDF Certificate", "Frontend & AI/ML Layer", "Naila Javed",
        "Mobile View QR Code Modal",
        [
            "Header button generates dynamic on-screen QR code pointing to live Vercel URL.",
            "Allows university examiners and field officers to scan and test live on mobile phones.",
            "Fluid responsive layout tailored specifically for smartphone touchscreens."
        ],
        "Official PDF Inspection Certificate",
        [
            "Custom @media print CSS formats dashboard into an official A4 water inspection report.",
            "Includes test timestamp, overall WQI score, parameter compliance table, and signature block.",
            "1-Click CSV Export: Instant download of raw historical telemetry for audit records."
        ],
        img_path=IMG_MOBILE
    )

    # =========================================================================
    # SLIDES 22 to 24: TESTING, VALIDATION & CONCLUSION (Entire Team)
    # =========================================================================
    add_content_slide(
        22, "Hardware Prototyping & Rig Fabrication", "Hardware & Assembly", "Entire Team",
        "Collaborative Prototyping Work",
        [
            "Breadboard Circuit Assembly: Unified 5V high-current bus and 3.3V digital logic rails.",
            "Ground Isolation: Common ground wiring prevents ground-loop distortion between sensors.",
            "Probe Holder Rig: Custom acrylic mounting plate keeping probes submerged without touching.",
            "Waterproof Cable Harness: Insulated wiring preventing moisture ingress and short circuits."
        ],
        "3-Point Laboratory Calibration",
        [
            "pH Electrode Calibration: Calibrated against standard buffer solutions at pH 4.01, 7.00, and 9.18.",
            "TDS Probe Calibration: Normalized using 1413 µS/cm conductivity calibration solution.",
            "Turbidity Baseline: Calibrated in pure distilled water to establish 0 NTU clean baseline."
        ]
    )

    add_content_slide(
        23, "Live 3-Sample Testing Demonstration", "Testing & Validation", "Entire Team",
        "Experimental Validation Results",
        [
            "Sample A (Commercial RO Water): TDS 110 ppm, pH 7.2, Turb 0.8 NTU → WQI 92 (Green, Safe).",
            "Sample B (Municipal Tap Water): TDS 380 ppm, pH 7.6, Turb 2.2 NTU → WQI 78 (Blue, Permissible).",
            "Sample C (Contaminated Saline Water): TDS >950 ppm, pH 9.1, Turb 14.5 NTU → WQI 42 (Red Alert)."
        ],
        "Dynamic System Reaction",
        [
            "Needles dynamically sweep to red alert zone within 4 seconds of probe immersion in Sample C.",
            "WQI circle updates instantly, triggering an automated red toast alert banner on dashboard.",
            "Proves rapid in-situ contamination detection without laboratory turnaround delay."
        ]
    )

    add_content_slide(
        24, "Conclusion & Future Engineering Scope", "Summary & Defense", "Entire Team",
        "Summary of Capstone Achievements",
        [
            "Successfully built full-stack IoT water monitor with 6 sensors and sub-4s cloud latency.",
            "Implemented custom 40-sample median filter and 25°C thermal compensation algorithms.",
            "Deployed live cloud infrastructure (Render + Vercel) with dual-transport reliability.",
            "Total prototype bill of materials optimized under ₹3,100 for scalable deployment."
        ],
        "Future Engineering Scope",
        [
            "Predictive AI/ML: Adding LSTM neural network to forecast contamination 6 hours in advance.",
            "Long-Range LoRaWAN: Replacing Wi-Fi with LoRaWAN (868MHz) for remote rural rivers up to 10km.",
            "Automated Dosing: Relay-actuated solenoid valves to inject neutralizer or chlorine automatically."
        ]
    )

    output_path = os.path.abspath("AquaSense_WQMS_Presentation.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Presentation saved successfully: {output_path}")

if __name__ == "__main__":
    create_deck()
