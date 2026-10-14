/**
 * ============================================================
 *  script.js — Multi-Parameter Live Water Quality Monitor
 *  Unified 220° Sweep (-110° to +110°) for all 6 Visual Meters:
 *    1. TDS Speedometer (0 - 1500 ppm)
 *    2. pH Level (0 - 14)
 *    3. Turbidity (0 - 20 NTU)
 *    4. Dissolved Oxygen (DO: 0 - 14 mg/L)
 *    5. Electrical Conductivity (EC: 0 - 2000 µS/cm)
 *    6. Temperature (0 - 50 °C)
 * ============================================================
 */

const API_BASE = "http://localhost:5000/api";

// Active Chart Configuration State
let trendChart = null;
let currentChartParam = "tds";
let currentHistoryHours = 24;
let lastAlertTimestamp = null;
let isSimulatorActive = true;

// Needles (Pivot: 130px, 125px)
const tdsNeedle = document.getElementById("tdsNeedle");
const phNeedle = document.getElementById("phNeedle");
const turbNeedle = document.getElementById("turbNeedle");
const doNeedle = document.getElementById("doNeedle");
const ecNeedle = document.getElementById("ecNeedle");
const tempNeedle = document.getElementById("tempNeedle");

// Digital Readouts
const tdsValueElem = document.getElementById("tdsValue");
const tdsStatusElem = document.getElementById("tdsStatus");
const phValueElem = document.getElementById("phValue");
const phStatusBadge = document.getElementById("phStatusBadge");
const turbValueElem = document.getElementById("turbValue");
const turbStatusBadge = document.getElementById("turbStatusBadge");
const doValueElem = document.getElementById("doValue");
const doStatusBadge = document.getElementById("doStatusBadge");
const ecValueElem = document.getElementById("ecValue");
const ecStatusBadge = document.getElementById("ecStatusBadge");
const tempValueElem = document.getElementById("tempValue");
const tempStatusBadge = document.getElementById("tempStatusBadge");

// WQI Elements
const wqiScoreElem = document.getElementById("wqiScore");
const wqiProgressCircle = document.getElementById("wqiProgressCircle");
const overallStatusBadge = document.getElementById("overallStatusBadge");
const wqiVerdictTitle = document.getElementById("wqiVerdictTitle");
const wqiVerdictDesc = document.getElementById("wqiVerdictDesc");
const potabilityChip = document.getElementById("potabilityChip");
const riskChip = document.getElementById("riskChip");

// Header badges
const deviceStatusDot = document.getElementById("deviceStatusDot");
const deviceStatusText = document.getElementById("deviceStatusText");
const liveClockElem = document.getElementById("liveClock");
const simDot = document.getElementById("simDot");
const simText = document.getElementById("simText");

// Logs & Alerts
const readingsTableBody = document.getElementById("readingsTableBody");
const readingsCountBadge = document.getElementById("readingsCountBadge");
const alertsListContainer = document.getElementById("alertsListContainer");
const alertsCountBadge = document.getElementById("alertsCountBadge");

/* ============================================================
   1. Initialize Precision Meter Ticks
   ============================================================ */
function initMeterTicks(groupId, intervals = 20) {
  const group = document.getElementById(groupId);
  if (!group) return;

  const cx = 130;
  const cy = 125;
  const rOuter = 93;

  for (let i = 0; i <= intervals; i++) {
    const isMajor = i % 5 === 0;
    const tickLen = isMajor ? 6.5 : 3.5;
    const rInner = rOuter - tickLen;

    const angleDeg = -110 + i * (220 / intervals);
    const angleRad = (angleDeg * Math.PI) / 180;

    const x1 = cx + rOuter * Math.sin(angleRad);
    const y1 = cy - rOuter * Math.cos(angleRad);
    const x2 = cx + rInner * Math.sin(angleRad);
    const y2 = cy - rInner * Math.cos(angleRad);

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x1.toFixed(2));
    line.setAttribute("y1", y1.toFixed(2));
    line.setAttribute("x2", x2.toFixed(2));
    line.setAttribute("y2", y2.toFixed(2));
    line.setAttribute("class", isMajor ? "gauge-tick tick-bold" : "gauge-tick");

    group.appendChild(line);
  }
}

function initAllTicks() {
  initMeterTicks("tdsTicksGroup", 25);
  initMeterTicks("phTicksGroup", 20);
  initMeterTicks("turbTicksGroup", 20);
  initMeterTicks("doTicksGroup", 20);
  initMeterTicks("ecTicksGroup", 20);
  initMeterTicks("tempTicksGroup", 20);
}

/* ============================================================
   2. Multi-Meter Visual Update Function (220° Sweep)
   ============================================================ */
function updateAllMeters(data) {
  // --- A. TDS Speedometer (0 - 1500 ppm, Sweep: -110° to +110°) ---
  const tds = data.tds_value || 0;
  const clampedTds = Math.min(Math.max(tds, 0), 1500);
  const tdsDeg = -110 + (clampedTds / 1500) * 220;
  if (tdsNeedle) tdsNeedle.style.transform = `rotate(${tdsDeg.toFixed(2)}deg)`;
  if (tdsValueElem) tdsValueElem.textContent = Math.round(tds);

  if (tdsStatusElem) {
    if (tds <= 300) {
      tdsStatusElem.className = "status-pill status-pill-excellent";
      tdsStatusElem.textContent = "Excellent Pure";
    } else if (tds <= 500) {
      tdsStatusElem.className = "status-pill status-pill-safe";
      tdsStatusElem.textContent = "Safe Potable";
    } else if (tds <= 900) {
      tdsStatusElem.className = "status-pill status-pill-warning";
      tdsStatusElem.textContent = "Warning High";
    } else {
      tdsStatusElem.className = "status-pill status-pill-unsafe";
      tdsStatusElem.textContent = "Contaminated";
    }
  }

  // --- B. pH Dial (0 - 14 pH, Sweep: -110° to +110°) ---
  const ph = data.ph_value !== undefined ? data.ph_value : 7.0;
  const clampedPh = Math.min(Math.max(ph, 0), 14);
  const phDeg = -110 + (clampedPh / 14) * 220;
  if (phNeedle) phNeedle.style.transform = `rotate(${phDeg.toFixed(2)}deg)`;
  if (phValueElem) phValueElem.textContent = ph.toFixed(2);

  if (phStatusBadge) {
    if (ph >= 6.8 && ph <= 7.8) {
      phStatusBadge.className = "status-pill status-pill-excellent";
      phStatusBadge.textContent = "Optimal Neutral";
    } else if (ph >= 6.5 && ph <= 8.5) {
      phStatusBadge.className = "status-pill status-pill-safe";
      phStatusBadge.textContent = "Acceptable";
    } else if (ph < 6.5) {
      phStatusBadge.className = "status-pill status-pill-warning";
      phStatusBadge.textContent = "Acidic";
    } else {
      phStatusBadge.className = "status-pill status-pill-warning";
      phStatusBadge.textContent = "Alkaline";
    }
  }

  // --- C. Turbidity Dial (0 - 20 NTU, Sweep: -110° to +110°) ---
  const turb = data.turbidity !== undefined ? data.turbidity : 1.0;
  const clampedTurb = Math.min(Math.max(turb, 0), 20);
  const turbDeg = -110 + (clampedTurb / 20) * 220;
  if (turbNeedle) turbNeedle.style.transform = `rotate(${turbDeg.toFixed(2)}deg)`;
  if (turbValueElem) turbValueElem.textContent = turb.toFixed(2);

  if (turbStatusBadge) {
    if (turb <= 1.0) {
      turbStatusBadge.className = "status-pill status-pill-excellent";
      turbStatusBadge.textContent = "Ultra Clear";
    } else if (turb <= 5.0) {
      turbStatusBadge.className = "status-pill status-pill-safe";
      turbStatusBadge.textContent = "Normal Clarity";
    } else if (turb <= 10.0) {
      turbStatusBadge.className = "status-pill status-pill-warning";
      turbStatusBadge.textContent = "Cloudy";
    } else {
      turbStatusBadge.className = "status-pill status-pill-unsafe";
      turbStatusBadge.textContent = "Turbid Murky";
    }
  }

  // --- D. Dissolved Oxygen (0 - 14 mg/L, Sweep: -110° to +110°) ---
  const doVal = data.do_value !== undefined ? data.do_value : 7.0;
  const clampedDo = Math.min(Math.max(doVal, 0), 14);
  const doDeg = -110 + (clampedDo / 14) * 220;
  if (doNeedle) doNeedle.style.transform = `rotate(${doDeg.toFixed(2)}deg)`;
  if (doValueElem) doValueElem.textContent = doVal.toFixed(1);

  if (doStatusBadge) {
    if (doVal >= 6.5) {
      doStatusBadge.className = "status-pill status-pill-excellent";
      doStatusBadge.textContent = "Optimal Aeration";
    } else if (doVal >= 5.0) {
      doStatusBadge.className = "status-pill status-pill-safe";
      doStatusBadge.textContent = "Adequate";
    } else if (doVal >= 4.0) {
      doStatusBadge.className = "status-pill status-pill-warning";
      doStatusBadge.textContent = "Hypoxic Risk";
    } else {
      doStatusBadge.className = "status-pill status-pill-unsafe";
      doStatusBadge.textContent = "Critical Low";
    }
  }

  // --- E. Electrical Conductivity (0 - 2000 µS/cm, Sweep: -110° to +110°) ---
  const ec = data.ec_value !== undefined ? data.ec_value : (tds / 0.64);
  const clampedEc = Math.min(Math.max(ec, 0), 2000);
  const ecDeg = -110 + (clampedEc / 2000) * 220;
  if (ecNeedle) ecNeedle.style.transform = `rotate(${ecDeg.toFixed(2)}deg)`;
  if (ecValueElem) ecValueElem.textContent = Math.round(ec);

  if (ecStatusBadge) {
    if (ec <= 400) {
      ecStatusBadge.className = "status-pill status-pill-excellent";
      ecStatusBadge.textContent = "Low Ions";
    } else if (ec <= 800) {
      ecStatusBadge.className = "status-pill status-pill-safe";
      ecStatusBadge.textContent = "Balanced";
    } else if (ec <= 1500) {
      ecStatusBadge.className = "status-pill status-pill-warning";
      ecStatusBadge.textContent = "High Salinity";
    } else {
      ecStatusBadge.className = "status-pill status-pill-unsafe";
      ecStatusBadge.textContent = "Very Conductive";
    }
  }

  // --- F. Temperature (0 - 50 °C, Sweep: -110° to +110°) ---
  const temp = data.temperature !== undefined ? data.temperature : 25.0;
  const clampedTemp = Math.min(Math.max(temp, 0), 50);
  const tempDeg = -110 + (clampedTemp / 50) * 220;
  if (tempNeedle) tempNeedle.style.transform = `rotate(${tempDeg.toFixed(2)}deg)`;
  if (tempValueElem) tempValueElem.textContent = temp.toFixed(1);

  if (tempStatusBadge) {
    if (temp >= 18 && temp <= 26) {
      tempStatusBadge.className = "status-pill status-pill-excellent";
      tempStatusBadge.textContent = "Comfortable";
    } else if (temp <= 32) {
      tempStatusBadge.className = "status-pill status-pill-safe";
      tempStatusBadge.textContent = "Normal Ambient";
    } else {
      tempStatusBadge.className = "status-pill status-pill-warning";
      tempStatusBadge.textContent = "Elevated Temp";
    }
  }

  // --- G. Water Quality Index (WQI) Score & Centered Ring ---
  const wqi = data.wqi_value !== undefined ? data.wqi_value : 85.0;
  if (wqiScoreElem) wqiScoreElem.textContent = Math.round(wqi);

  if (wqiProgressCircle) {
    const circumference = 2 * Math.PI * 40; // ~251.32
    const offset = circumference - (Math.min(Math.max(wqi, 0), 100) / 100) * circumference;
    wqiProgressCircle.style.strokeDashoffset = offset;

    if (wqi >= 85) {
      wqiProgressCircle.style.stroke = "#22C55E";
    } else if (wqi >= 70) {
      wqiProgressCircle.style.stroke = "#2E86DE";
    } else if (wqi >= 50) {
      wqiProgressCircle.style.stroke = "#F59E0B";
    } else {
      wqiProgressCircle.style.stroke = "#EF4444";
    }
  }

  if (overallStatusBadge) {
    let statusClass = "status-pill-safe";
    if (data.status === "Excellent") statusClass = "status-pill-excellent";
    else if (data.status === "Warning") statusClass = "status-pill-warning";
    else if (data.status === "Unsafe") statusClass = "status-pill-unsafe";

    overallStatusBadge.className = `status-pill ${statusClass}`;
    overallStatusBadge.textContent = (data.status || "Safe").toUpperCase();
  }

  // Verdict details
  if (wqiVerdictTitle && wqiVerdictDesc) {
    if (data.status === "Unsafe" || wqi < 50) {
      wqiVerdictTitle.textContent = "Contamination Alert — Water Unsafe";
      wqiVerdictDesc.textContent = "One or more parameters exceed permissible drinking thresholds. Immediate filtration / RO treatment required.";
      if (potabilityChip) {
        potabilityChip.textContent = "Unfit for Consumption";
        potabilityChip.className = "chip-val color-unsafe";
      }
      if (riskChip) {
        riskChip.textContent = tds > 900 ? "Excessive TDS" : (turb > 10 ? "Heavy Turbidity" : "pH Imbalance");
        riskChip.className = "chip-val color-unsafe";
      }
    } else if (data.status === "Warning" || wqi < 70) {
      wqiVerdictTitle.textContent = "Moderate Quality — Approaching Threshold";
      wqiVerdictDesc.textContent = "Sensors detect slight deviations in dissolved solids or turbidity. Suitable for general utility; boiling recommended.";
      if (potabilityChip) {
        potabilityChip.textContent = "Permissible / Caution";
        potabilityChip.className = "chip-val color-warning";
      }
      if (riskChip) {
        riskChip.textContent = "Minor Mineral Elevation";
        riskChip.className = "chip-val color-warning";
      }
    } else {
      wqiVerdictTitle.textContent = "Optimal Potability — High Purity Water";
      wqiVerdictDesc.textContent = "All 6 parameters strictly adhere to WHO and Bureau of Indian Standards (BIS IS 10500:2012) drinking specifications.";
      if (potabilityChip) {
        potabilityChip.textContent = "Safe for Drinking";
        potabilityChip.className = "chip-val color-safe";
      }
      if (riskChip) {
        riskChip.textContent = "None Detected";
        riskChip.className = "chip-val";
      }
    }
  }
}

/* ============================================================
   3. Online / Offline & Standby Handlers (Hardware Driven)
   ============================================================ */
function setOnline(online, label) {
  if (!deviceStatusDot || !deviceStatusText) return;
  if (online) {
    deviceStatusDot.className = "status-dot dot-online";
    deviceStatusText.textContent = label || "Hardware Connected";
  } else {
    deviceStatusDot.className = "status-dot dot-offline";
    deviceStatusText.textContent = label || "Hardware Disconnected";
  }
}

function setStandbyMode(msg = "Hardware Disconnected (Waiting for ESP32)") {
  setOnline(false, msg);

  // Return all needles to resting position (-110 deg)
  const restDeg = "-110deg";
  if (tdsNeedle) tdsNeedle.style.transform = `rotate(${restDeg})`;
  if (phNeedle) phNeedle.style.transform = `rotate(${restDeg})`;
  if (turbNeedle) turbNeedle.style.transform = `rotate(${restDeg})`;
  if (doNeedle) doNeedle.style.transform = `rotate(${restDeg})`;
  if (ecNeedle) ecNeedle.style.transform = `rotate(${restDeg})`;
  if (tempNeedle) tempNeedle.style.transform = `rotate(${restDeg})`;

  // Set readouts to waiting
  if (tdsValueElem) tdsValueElem.textContent = "--";
  if (phValueElem) phValueElem.textContent = "--.-";
  if (turbValueElem) turbValueElem.textContent = "--.-";
  if (doValueElem) doValueElem.textContent = "--.-";
  if (ecValueElem) ecValueElem.textContent = "---";
  if (tempValueElem) tempValueElem.textContent = "--.-";

  if (tdsStatusElem) {
    tdsStatusElem.className = "status-pill status-pill-neutral";
    tdsStatusElem.textContent = "Standby";
  }
  if (phStatusBadge) {
    phStatusBadge.className = "status-pill status-pill-neutral";
    phStatusBadge.textContent = "Standby";
  }
  if (turbStatusBadge) {
    turbStatusBadge.className = "status-pill status-pill-neutral";
    turbStatusBadge.textContent = "Standby";
  }
  if (doStatusBadge) {
    doStatusBadge.className = "status-pill status-pill-neutral";
    doStatusBadge.textContent = "Standby";
  }
  if (ecStatusBadge) {
    ecStatusBadge.className = "status-pill status-pill-neutral";
    ecStatusBadge.textContent = "Standby";
  }
  if (tempStatusBadge) {
    tempStatusBadge.className = "status-pill status-pill-neutral";
    tempStatusBadge.textContent = "Standby";
  }

  // WQI Standby
  if (wqiScoreElem) wqiScoreElem.textContent = "--";
  if (wqiProgressCircle) wqiProgressCircle.style.strokeDashoffset = 251.32;
  if (overallStatusBadge) {
    overallStatusBadge.className = "status-pill status-pill-neutral";
    overallStatusBadge.textContent = "STANDBY";
  }
  if (wqiVerdictTitle) wqiVerdictTitle.textContent = "Awaiting ESP32 Hardware Stream";
  if (wqiVerdictDesc) wqiVerdictDesc.textContent = "Connect the ESP32 microcontroller to Wi-Fi. Live telemetry meters will activate immediately upon packet arrival.";
  if (potabilityChip) {
    potabilityChip.textContent = "Awaiting Hardware";
    potabilityChip.className = "chip-val";
  }
  if (riskChip) {
    riskChip.textContent = "Sensors Offline";
    riskChip.className = "chip-val";
  }
}

/* ============================================================
   4. Live Clock
   ============================================================ */
function updateLiveClock() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString("en-GB", { hour12: false });
  if (liveClockElem) liveClockElem.textContent = timeStr;
}

/* ============================================================
   5. Toast Notification System
   ============================================================ */
function showToast(message, type = "warning") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div style="font-size: 1.1rem;">⚠️</div>
    <div class="toast-message">${message}</div>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

/* ============================================================
   6. Fetch Latest Sensor Reading (Hardware Freshness Check)
   ============================================================ */
async function fetchLatest() {
  try {
    const res = await fetch(`${API_BASE}/latest`);
    if (!res.ok) throw new Error("API error");
    const data = await res.json();

    if (!data.is_live || data.status === "offline") {
      setStandbyMode(data.message || "Hardware Disconnected (Waiting for ESP32)");
      return;
    }

    setOnline(true, `Hardware Connected (${data.device_id || "ESP32"})`);
    updateAllMeters(data);

    if (data.status === "Warning" || data.status === "Unsafe") {
      if (lastAlertTimestamp !== data.timestamp) {
        lastAlertTimestamp = data.timestamp;
        showToast(
          `Water Quality Alert: ${data.status} level recorded (${data.tds_value} ppm, pH ${data.ph_value})`,
          data.status === "Unsafe" ? "danger" : "warning"
        );
      }
    }
  } catch (err) {
    console.warn("Telemetry fetch error:", err);
    setStandbyMode("Server Offline / Reconnecting...");
  }
}

/* ============================================================
   7. Fetch History & Trend Chart Update
   ============================================================ */
async function fetchHistory(hours = 24) {
  try {
    const [historyRes, alertsRes] = await Promise.all([
      fetch(`${API_BASE}/history?hours=${hours}`),
      fetch(`${API_BASE}/alerts`)
    ]);

    const historyData = await historyRes.json();
    const alertsData = await alertsRes.json();

    updateTrendChart(historyData);
    updateTable(historyData);
    updateAlertsList(alertsData);
  } catch (err) {
    console.warn("History fetch error:", err);
  }
}

/* ============================================================
   8. Chart.js Multi-Parameter Setup & Switching
   ============================================================ */
const PARAM_CONFIG = {
  tds: {
    label: "TDS (ppm)",
    field: "tds_value",
    color: "#2E86DE",
    safeLimit: 500,
    safeLabel: "Safe Limit (500 ppm)"
  },
  ph: {
    label: "pH Level",
    field: "ph_value",
    color: "#8B5CF6",
    safeLimit: 8.5,
    safeLabel: "Upper Safe (8.5 pH)"
  },
  turbidity: {
    label: "Turbidity (NTU)",
    field: "turbidity",
    color: "#F59E0B",
    safeLimit: 5.0,
    safeLabel: "Safe Limit (5 NTU)"
  },
  do: {
    label: "Dissolved Oxygen (mg/L)",
    field: "do_value",
    color: "#059669",
    safeLimit: 5.0,
    safeLabel: "Min Healthy (5.0 mg/L)"
  },
  ec: {
    label: "Conductivity (µS/cm)",
    field: "ec_value",
    color: "#0284C7",
    safeLimit: 800,
    safeLabel: "Safe Limit (800 µS/cm)"
  },
  temp: {
    label: "Temperature (°C)",
    field: "temperature",
    color: "#DC2626",
    safeLimit: 30.0,
    safeLabel: "Ref Limit (30 °C)"
  }
};

function initChart() {
  const canvas = document.getElementById("trendChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const cfg = PARAM_CONFIG[currentChartParam];

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: cfg.label,
          data: [],
          borderColor: cfg.color,
          backgroundColor: "rgba(46, 134, 222, 0.08)",
          fill: true,
          tension: 0.3,
          pointRadius: 2,
          borderWidth: 2.5
        },
        {
          label: cfg.safeLabel,
          data: [],
          borderColor: "#EF4444",
          borderDash: [6, 6],
          borderWidth: 1.5,
          fill: false,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: { boxWidth: 14, usePointStyle: true, font: { family: "Poppins", size: 12 } }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { family: "Poppins", size: 11 }, color: "#6B7280", maxTicksLimit: 10 } },
        y: { grid: { color: "#F0F2F5" }, ticks: { font: { family: "Poppins", size: 11 }, color: "#6B7280" } }
      }
    }
  });
}

function updateTrendChart(dataList) {
  if (!trendChart) return;
  const cfg = PARAM_CONFIG[currentChartParam];

  const labels = [];
  const points = [];
  const limits = [];

  const step = Math.max(1, Math.floor(dataList.length / 100));
  for (let i = 0; i < dataList.length; i += step) {
    const item = dataList[i];
    const timeFormatted = item.timestamp.split(" ")[1] || item.timestamp;
    labels.push(timeFormatted);
    points.push(item[cfg.field]);
    limits.push(cfg.safeLimit);
  }

  trendChart.data.labels = labels;
  trendChart.data.datasets[0].label = cfg.label;
  trendChart.data.datasets[0].data = points;
  trendChart.data.datasets[0].borderColor = cfg.color;
  trendChart.data.datasets[1].label = cfg.safeLabel;
  trendChart.data.datasets[1].data = limits;
  trendChart.update("none");
}

function switchParamChart(paramKey, btn) {
  if (!PARAM_CONFIG[paramKey]) return;
  currentChartParam = paramKey;
  document.querySelectorAll(".param-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  fetchHistory(currentHistoryHours);
}

/* ============================================================
   9. Update Table & Alerts
   ============================================================ */
function updateTable(readings) {
  if (!readingsTableBody) return;

  if (readingsCountBadge) {
    readingsCountBadge.textContent = `${readings.length} records`;
  }

  if (readings.length === 0) {
    readingsTableBody.innerHTML = `<tr><td colspan="9" class="empty-state">No readings collected yet.</td></tr>`;
    return;
  }

  const recent = [...readings].reverse().slice(0, 15);

  readingsTableBody.innerHTML = recent.map(r => {
    let pillClass = "status-pill-safe";
    if (r.status === "Excellent") pillClass = "status-pill-excellent";
    else if (r.status === "Warning") pillClass = "status-pill-warning";
    else if (r.status === "Unsafe") pillClass = "status-pill-unsafe";

    return `
      <tr>
        <td>${r.timestamp.split(" ")[1] || r.timestamp}</td>
        <td><strong>${r.tds_value.toFixed(1)}</strong></td>
        <td>${(r.ph_value || 7.0).toFixed(2)}</td>
        <td>${(r.turbidity || 1.0).toFixed(2)}</td>
        <td>${(r.do_value || 7.0).toFixed(1)}</td>
        <td>${Math.round(r.ec_value || (r.tds_value / 0.64))}</td>
        <td>${r.temperature.toFixed(1)}</td>
        <td><strong>${Math.round(r.wqi_value || 85)}</strong></td>
        <td><span class="table-status-pill ${pillClass}">${r.status}</span></td>
      </tr>
    `;
  }).join("");
}

function updateAlertsList(alerts) {
  if (!alertsListContainer) return;
  if (alertsCountBadge) alertsCountBadge.textContent = `${alerts.length} alerts`;

  if (alerts.length === 0) {
    alertsListContainer.innerHTML = `
      <div class="alert-empty-card">
        <div class="alert-empty-icon">🎉</div>
        <div class="alert-empty-title">All Parameters Within Safe Limits</div>
        <div class="alert-empty-desc">TDS, pH balance, clarity, and DO satisfy standard drinking water criteria.</div>
      </div>
    `;
    return;
  }

  alertsListContainer.innerHTML = alerts.slice(0, 10).map(a => {
    const isUnsafe = a.status === "Unsafe";
    const itemClass = isUnsafe ? "alert-item-unsafe" : "alert-item-warning";
    const emoji = isUnsafe ? "🚨" : "⚠️";

    return `
      <div class="alert-item ${itemClass}">
        <div class="alert-item-content">
          <span class="alert-item-title">${emoji} ${a.status} Reading (${a.tds_value} ppm, pH ${(a.ph_value || 7.2).toFixed(1)})</span>
          <span class="alert-item-sub">Time: ${a.timestamp} | Turbidity: ${(a.turbidity || 1.5).toFixed(1)} NTU | DO: ${(a.do_value || 7.0).toFixed(1)} mg/L</span>
        </div>
      </div>
    `;
  }).join("");
}

/* ============================================================
   10. Controls & Utilities
   ============================================================ */
function changeRange(btn, hours) {
  currentHistoryHours = hours;
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  fetchHistory(currentHistoryHours);
}

function exportData() {
  window.open(`${API_BASE}/export/csv`, "_blank");
}

async function toggleSimulator() {
  try {
    const res = await fetch(`${API_BASE}/simulator/toggle`, { method: "POST" });
    const data = await res.json();
    isSimulatorActive = data.simulator_enabled;

    if (simDot && simText) {
      if (isSimulatorActive) {
        simDot.className = "sim-status-dot active";
        simText.textContent = "Sim Stream: Active";
      } else {
        simDot.className = "sim-status-dot";
        simText.textContent = "Sim Stream: Paused";
      }
    }
  } catch (e) {
    console.warn("Simulator toggle error:", e);
  }
}

/* ============================================================
   11. Startup Initialization
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  initAllTicks();
  initChart();

  fetchLatest();
  fetchHistory(currentHistoryHours);

  setInterval(updateLiveClock, 1000);
  setInterval(fetchLatest, 4000);
  setInterval(() => fetchHistory(currentHistoryHours), 20000);

  updateLiveClock();
});
