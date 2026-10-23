# =============================================================
#  database.py — SQLAlchemy Models and Database Initialisation
#
#  Defines the multi-parameter WaterQualityReading table:
#  TDS, pH, Turbidity, Temperature, Dissolved Oxygen (DO),
#  and Electrical Conductivity (EC), plus overall WQI.
# =============================================================

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

import config

Base = declarative_base()

class WaterQualityReading(Base):
    """
    Represents a multi-parameter water quality measurement in SQLite.
    Parameters monitored:
      - TDS: Total Dissolved Solids (ppm)
      - pH: Acidity / Alkalinity level (0-14)
      - Turbidity: Suspended solids cloudiness (NTU)
      - Temperature: Water temperature (°C)
      - DO: Dissolved Oxygen (mg/L)
      - EC: Electrical Conductivity (µS/cm)
      - WQI: Weighted Water Quality Index (0-100)
    """
    __tablename__ = "water_readings"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    device_id   = Column(String(50), nullable=False, default="WQMS_NODE01")
    tds_value   = Column(Float, nullable=False, default=250.0)      # ppm
    ph_value    = Column(Float, nullable=False, default=7.2)        # pH units
    turbidity   = Column(Float, nullable=False, default=1.8)        # NTU
    temperature = Column(Float, nullable=False, default=24.5)       # °C
    do_value    = Column(Float, nullable=False, default=7.4)        # mg/L
    ec_value    = Column(Float, nullable=False, default=390.0)      # µS/cm
    wqi_value   = Column(Float, nullable=False, default=88.5)       # 0 - 100 Index
    status      = Column(String(20), nullable=False, default="Safe")# Excellent/Safe/Warning/Unsafe
    timestamp   = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert row to a JSON-serializable dictionary."""
        return {
            "id":          self.id,
            "device_id":   self.device_id,
            "tds_value":   round(float(self.tds_value), 1),
            "ph_value":    round(float(self.ph_value), 2),
            "turbidity":   round(float(self.turbidity), 2),
            "temperature": round(float(self.temperature), 1),
            "do_value":    round(float(self.do_value), 2),
            "ec_value":    round(float(self.ec_value), 1),
            "wqi_value":   round(float(self.wqi_value), 1),
            "status":      self.status,
            "timestamp":   self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

# Backward compatibility alias
TDSReading = WaterQualityReading

# Engine with thread-safety
if config.DB_TYPE == "sqlite":
    engine = create_engine(
        config.DB_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    # PostgreSQL (Supabase) — no check_same_thread needed
    engine = create_engine(
        config.DB_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialise database tables (SQLite or Supabase PostgreSQL)."""
    global engine, SessionLocal
    if config.DB_TYPE == "sqlite":
        db_dir = os.path.dirname(config.DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    try:
        Base.metadata.create_all(bind=engine)
        print(f"[DB] Multi-parameter Database initialised ({config.DB_TYPE})")
    except Exception as e:
        print(f"[DB ERROR] Could not connect to remote {config.DB_TYPE} database: {e}")
        if config.DB_TYPE != "sqlite":
            print("[DB] Falling back to SQLite local database so server stays online...")
            config.DB_TYPE = "sqlite"
            db_dir = os.path.dirname(config.DB_PATH)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            engine = create_engine(
                f"sqlite:///{config.DB_PATH}",
                connect_args={"check_same_thread": False},
                echo=False
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
            print("[DB] Local SQLite fallback initialised successfully.")
        else:
            raise

def get_session():
    """Returns a new SQLAlchemy session."""
    return SessionLocal()

