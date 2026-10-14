# =============================================================
#  alert_service.py — Multi-Parameter Threshold & WQI Engine
#
#  Rule-based logic for:
#    - TDS (Total Dissolved Solids)
#    - pH
#    - Turbidity (NTU)
#    - Temperature (°C)
#    - Dissolved Oxygen (DO)
#    - Electrical Conductivity (EC)
#    - Overall Water Quality Index (WQI)
# =============================================================

import logging
from datetime import datetime
import config

alert_logger = logging.getLogger("alert")
alert_logger.setLevel(logging.WARNING)

file_handler = logging.FileHandler(config.ALERT_LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
if not alert_logger.handlers:
    alert_logger.addHandler(file_handler)


def evaluate_parameter_status(tds: float, ph: float, turbidity: float, temp: float, do_val: float, ec: float):
    """
    Evaluates individual parameters and determines the overall water quality rating.
    Follows WHO and Bureau of Indian Standards (BIS IS 10500:2012).
    """
    statuses = []

    # 1. TDS Evaluation
    if tds <= 300:
        tds_status = "Excellent"
    elif tds <= config.TDS_SAFE_LIMIT:
        tds_status = "Safe"
    elif tds <= config.TDS_WARNING_LIMIT:
        tds_status = "Warning"
    else:
        tds_status = "Unsafe"
    statuses.append(tds_status)

    # 2. pH Evaluation (BIS standard: 6.5 to 8.5)
    if 6.8 <= ph <= 7.8:
        ph_status = "Excellent"
    elif 6.5 <= ph <= 8.5:
        ph_status = "Safe"
    elif 6.0 <= ph < 6.5 or 8.5 < ph <= 9.0:
        ph_status = "Warning"
    else:
        ph_status = "Unsafe"
    statuses.append(ph_status)

    # 3. Turbidity Evaluation (BIS limit: <= 5 NTU)
    if turbidity <= 1.0:
        turb_status = "Excellent"
    elif turbidity <= 5.0:
        turb_status = "Safe"
    elif turbidity <= 10.0:
        turb_status = "Warning"
    else:
        turb_status = "Unsafe"
    statuses.append(turb_status)

    # 4. Dissolved Oxygen (DO) Evaluation (Safe >= 5.0 mg/L)
    if do_val >= 6.5:
        do_status = "Excellent"
    elif do_val >= 5.0:
        do_status = "Safe"
    elif do_val >= 4.0:
        do_status = "Warning"
    else:
        do_status = "Unsafe"
    statuses.append(do_status)

    # 5. Electrical Conductivity (EC) Evaluation
    if ec <= 400:
        ec_status = "Excellent"
    elif ec <= 800:
        ec_status = "Safe"
    elif ec <= 1500:
        ec_status = "Warning"
    else:
        ec_status = "Unsafe"
    statuses.append(ec_status)

    # Aggregate status: If any parameter is Unsafe -> overall Unsafe.
    # If any is Warning -> Warning. If all are Safe/Excellent -> Safe or Excellent.
    if "Unsafe" in statuses:
        overall_status = "Unsafe"
    elif "Warning" in statuses:
        overall_status = "Warning"
    elif all(s == "Excellent" for s in statuses):
        overall_status = "Excellent"
    else:
        overall_status = "Safe"

    return overall_status, {
        "tds": tds_status,
        "ph": ph_status,
        "turbidity": turb_status,
        "do": do_status,
        "ec": ec_status
    }


def calculate_wqi(tds: float, ph: float, turbidity: float, do_val: float, ec: float) -> float:
    """
    Computes a simplified Water Quality Index (WQI) score from 0 to 100
    using standard normalized sub-indices.
    100 = Perfectly pure water, <50 = Unfit for consumption.
    """
    # Sub-index for TDS (ideal <= 250, max 1000)
    q_tds = max(0.0, min(100.0, 100.0 - (tds / 10.0)))

    # Sub-index for pH (ideal 7.0, tolerance +- 1.5)
    ph_diff = abs(ph - 7.0)
    q_ph = max(0.0, min(100.0, 100.0 - (ph_diff * 35.0)))

    # Sub-index for Turbidity (ideal <= 0.5 NTU, max 10 NTU)
    q_turb = max(0.0, min(100.0, 100.0 - (turbidity * 10.0)))

    # Sub-index for DO (ideal >= 8.0 mg/L)
    q_do = max(0.0, min(100.0, (do_val / 8.0) * 100.0))

    # Sub-index for EC (ideal <= 300, max 1500)
    q_ec = max(0.0, min(100.0, 100.0 - (ec / 15.0)))

    # Weights sum to 1.0: DO (0.25), pH (0.25), TDS (0.20), Turbidity (0.20), EC (0.10)
    wqi = (q_do * 0.25) + (q_ph * 0.25) + (q_tds * 0.20) + (q_turb * 0.20) + (q_ec * 0.10)
    return round(float(wqi), 1)


def check_threshold(tds_value: float) -> str:
    """Backward compatibility helper for TDS-only calls."""
    if tds_value <= config.TDS_EXCELLENT_LIMIT:
        return "Excellent"
    elif tds_value <= config.TDS_SAFE_LIMIT:
        return "Safe"
    elif tds_value <= config.TDS_WARNING_LIMIT:
        return "Warning"
    else:
        return "Unsafe"


def log_alert(device_id: str, tds_value: float, status: str, details: str = ""):
    """Logs security and contamination alerts to alerts.log file."""
    if status in ("Warning", "Unsafe"):
        msg = f"Device={device_id} | TDS={tds_value:.1f} ppm | Status={status} | {details}"
        alert_logger.warning(msg)
        print(f"[CONTAMINATION ALERT] {msg}")


def send_email_alert(device_id: str, tds_value: float, status: str):
    """Optional SMTP notification."""
    pass
