# =============================================================
#  config.py — Central Configuration for TDS Monitoring System
#
#  All tunable parameters live here.
#  Import this file in other modules to avoid hardcoding values.
# =============================================================

import os
from dotenv import load_dotenv

# Load .env file if it exists (for development overrides)
load_dotenv()

# -------------------------------------------------------
#  MQTT Broker Settings
# -------------------------------------------------------
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")   # Mosquitto broker host
MQTT_PORT   = int(os.getenv("MQTT_PORT", 1883))        # Default MQTT port
MQTT_TOPIC  = os.getenv("MQTT_TOPIC", "water/tds/data") # Topic to subscribe to

# -------------------------------------------------------
#  Database
# -------------------------------------------------------
# Path to the SQLite database file (relative to backend/)
DB_PATH = os.getenv("DB_PATH", "../database/tds_data.db")

# Supabase PostgreSQL (cloud) or SQLite (local fallback)
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL", "")

if SUPABASE_DB_URL:
    # Ensure SQLAlchemy uses psycopg2 driver for PostgreSQL
    if SUPABASE_DB_URL.startswith("postgresql://"):
        DB_URL = SUPABASE_DB_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    else:
        DB_URL = SUPABASE_DB_URL
    DB_TYPE = "supabase"
    print("[CONFIG] Using Supabase PostgreSQL database")
else:
    DB_URL = f"sqlite:///{DB_PATH}"
    DB_TYPE = "sqlite"
    print(f"[CONFIG] Using local SQLite database: {DB_PATH}")

# -------------------------------------------------------
#  TDS Threshold Limits (ppm)
#  These match WHO / BIS IS 10500:2012 guidelines
# -------------------------------------------------------
TDS_EXCELLENT_LIMIT = int(os.getenv("TDS_EXCELLENT_LIMIT", 300))  # ≤300 → Excellent
TDS_SAFE_LIMIT      = int(os.getenv("TDS_SAFE_LIMIT", 500))       # ≤500 → Safe
TDS_WARNING_LIMIT   = int(os.getenv("TDS_WARNING_LIMIT", 900))    # ≤900 → Warning
                                                                    # >900 → Unsafe

# -------------------------------------------------------
#  Flask Server
# -------------------------------------------------------
import re as _re
_raw_port = os.getenv("FLASK_PORT", "5000")
FLASK_PORT = int(_re.sub(r"[^0-9]", "", _raw_port) or "5000")  # Port for Flask app
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"

# -------------------------------------------------------
#  Alert Logging
# -------------------------------------------------------
ALERT_LOG_FILE = "alerts.log"  # File where unsafe readings are logged

# -------------------------------------------------------
#  Email Alerts (Optional — configure SMTP to enable)
# -------------------------------------------------------
ENABLE_EMAIL_ALERTS  = False                          # Set True to enable
SMTP_HOST            = "smtp.gmail.com"
SMTP_PORT            = 587
SMTP_USER            = "your_email@gmail.com"
SMTP_PASSWORD        = "your_app_password"
ALERT_EMAIL_RECEIVER = "recipient@example.com"
