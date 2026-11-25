import logging
import os
import platform
import time
from collections import deque
from datetime import datetime, timezone

import psutil
from flask import Flask, jsonify, render_template_string, request

APP_NAME = os.getenv("APP_NAME", "Cloud Deployment Monitor")
PORT = int(os.getenv("PORT", "5000"))
START_TIME = time.time()
REQUEST_COUNT = 0
RECENT_LOGS = deque(maxlen=80)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("cloud-monitor")

app = Flask(__name__)

HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ app_name }}</title>
  <style>
    :root { color-scheme: dark; --bg:#0b1020; --panel:#151d32; --muted:#a7b2ca; --text:#f4f7ff; --accent:#72e0c2; --line:#293653; }
    * { box-sizing:border-box }
    body { margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; background:radial-gradient(circle at top right,#1b3150 0,#0b1020 42%); color:var(--text); }
    .wrap { max-width:1180px; margin:auto; padding:28px 18px 48px; }
    header { display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; margin-bottom:24px; }
    .eyebrow { color:var(--accent); text-transform:uppercase; letter-spacing:.15em; font-size:12px; font-weight:800; }
    h1 { margin:7px 0; font-size:clamp(27px,4vw,40px); }
    .sub { color:var(--muted); margin:0; }
    .pill { border:1px solid #286f62; color:var(--accent); padding:9px 13px; border-radius:999px; font-size:13px; }
    .grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
    .panel { background:rgba(21,29,50,.92); border:1px solid var(--line); border-radius:17px; padding:19px; box-shadow:0 10px 35px #0002; }
    .metric-label { color:var(--muted); font-size:13px; }
    .metric { font-size:30px; font-weight:800; margin:10px 0 4px; }
    .hint { color:var(--muted); font-size:12px; }
    .section { margin-top:16px; }
    .section h2 { font-size:18px; margin:0 0 14px; }
    .two { display:grid; grid-template-columns:1.1fr .9fr; gap:14px; }
    .bar { height:8px; background:#28334d; border-radius:99px; overflow:hidden; margin:10px 0 16px; }
    .fill { height:100%; width:0; background:linear-gradient(90deg,#4ec9a8,#9af2d8); border-radius:99px; transition:width .35s; }
    .row { display:flex; align-items:center; justify-content:space-between; gap:12px; font-size:14px; }
    .status-dot { display:inline-block; width:9px; height:9px; border-radius:50%; background:var(--accent); margin-right:7px; }
    .logs { max-height:300px; overflow:auto; font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:12px; line-height:1.65; color:#c7d5ee; white-space:pre-wrap; overflow-wrap:anywhere; }
    button { background:var(--accent); border:0; color:#08221c; padding:10px 14px; font-weight:800; border-radius:10px; cursor:pointer; }
    .actions { display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
    .small { color:var(--muted); font-size:12px; }
    .foot { margin-top:18px; color:var(--muted); font-size:12px; text-align:center; }
    @media(max-width:800px) { .grid{grid-template-columns:repeat(2,minmax(0,1fr))}.two{grid-template-columns:1fr} }
    @media(max-width:420px) { .grid{grid-template-columns:1fr}.metric{font-size:27px} }
  </style>
</head>
<body>
<div class="wrap">
  <header>
    <div><div class="eyebrow">Virtualisation & Cloud Computing · PBL</div><h1>{{ app_name }}</h1><p class="sub">Local container deployment and live application monitoring</p></div>
    <div class="actions"><span class="pill"><span class="status-dot"></span><span id="healthLabel">Checking health…</span></span><button onclick="refreshData()">Refresh now</button></div>
  </header>
  <div class="grid">
    <div class="panel"><div class="metric-label">CPU usage</div><div class="metric" id="cpu">—</div><div class="hint">Visible to this application container</div><div class="bar"><div class="fill" id="cpuBar"></div></div></div>
    <div class="panel"><div class="metric-label">Memory usage</div><div class="metric" id="mem">—</div><div class="hint" id="memHint">RAM statistics</div><div class="bar"><div class="fill" id="memBar"></div></div></div>
    <div class="panel"><div class="metric-label">Application uptime</div><div class="metric" id="uptime">—</div><div class="hint">Time since this process started</div></div>
    <div class="panel"><div class="metric-label">HTTP requests</div><div class="metric" id="requests">—</div><div class="hint">Requests served since startup</div></div>
  </div>
  <div class="two section">
    <div class="panel">
      <h2>Runtime and deployment details</h2>
      <div class="row"><span class="metric-label">Application</span><strong id="appName">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span class="metric-label">Python version</span><strong id="python">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span class="metric-label">Operating system</span><strong id="os">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span class="metric-label">Hostname / container ID</span><strong id="host">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span class="metric-label">Last updated</span><strong id="updated">—</strong></div>
    </div>
    <div class="panel">
      <h2>Health checks</h2>
      <div class="row"><span><span class="status-dot"></span>HTTP health endpoint</span><strong id="httpHealth">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span><span class="status-dot"></span>Process running</span><strong id="processHealth">—</strong></div><hr style="border:0;border-top:1px solid var(--line);margin:13px 0">
      <div class="row"><span><span class="status-dot"></span>Metrics endpoint</span><strong id="metricsHealth">—</strong></div>
      <p class="small">This dashboard reports metrics available inside the container. Container CPU/memory limits and host-level usage may differ.</p>
    </div>
  </div>
  <div class="panel section">
    <div class="row" style="margin-bottom:12px"><h2 style="margin:0">Recent application events</h2><span class="small">Latest 20 events</span></div>
    <div class="logs" id="logs">Loading logs…</div>
  </div>
  <div class="foot">Educational demonstration · Flask + psutil + Docker · No external cloud account required</div>
</div>
<script>
async function refreshData() {
  try {
    const response = await fetch('/api/metrics', {cache:'no-store'});
    const d = await response.json();
    document.getElementById('healthLabel').textContent = d.status.toUpperCase();
    document.getElementById('cpu').textContent = d.cpu_percent.toFixed(1) + '%';
    document.getElementById('cpuBar').style.width = Math.min(100,d.cpu_percent) + '%';
    document.getElementById('mem').textContent = d.memory_percent.toFixed(1) + '%';
    document.getElementById('memBar').style.width = Math.min(100,d.memory_percent) + '%';
    document.getElementById('memHint').textContent = d.memory_used_mb + ' MB used / ' + d.memory_total_mb + ' MB visible';
    document.getElementById('uptime').textContent = d.uptime;
    document.getElementById('requests').textContent = d.request_count;
    document.getElementById('appName').textContent = d.app_name;
    document.getElementById('python').textContent = d.python_version;
    document.getElementById('os').textContent = d.platform;
    document.getElementById('host').textContent = d.hostname;
    document.getElementById('updated').textContent = new Date(d.timestamp).toLocaleTimeString();
    document.getElementById('httpHealth').textContent = 'OK';
    document.getElementById('processHealth').textContent = 'RUNNING';
    document.getElementById('metricsHealth').textContent = 'OK';
    document.getElementById('logs').textContent = d.logs.length ? d.logs.join('\\n') : 'No events recorded yet.';
  } catch (e) {
    document.getElementById('healthLabel').textContent = 'UNAVAILABLE';
    document.getElementById('logs').textContent = 'Could not load metrics: ' + e;
  }
}
refreshData();
setInterval(refreshData, 5000);
</script>
</body>
</html>
"""

def add_event(message):
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    line = f"[{stamp}] {message}"
    RECENT_LOGS.appendleft(line)
    logger.info(message)

@app.before_request
def count_request():
    global REQUEST_COUNT
    REQUEST_COUNT += 1

@app.after_request
def log_request(response):
    if request.path not in ("/api/metrics", "/health"):
        add_event(f"{request.method} {request.path} -> {response.status_code}")
    return response

@app.get("/")
def dashboard():
    return render_template_string(HTML, app_name=APP_NAME)

@app.get("/health")
def health():
    return jsonify({"status": "healthy", "app": APP_NAME, "timestamp": datetime.now(timezone.utc).isoformat()}), 200

@app.get("/api/metrics")
def metrics():
    virtual_memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)
    uptime_seconds = max(0, int(time.time() - START_TIME))
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime = f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
    return jsonify({
        "status": "healthy",
        "app_name": APP_NAME,
        "cpu_percent": cpu,
        "memory_percent": virtual_memory.percent,
        "memory_used_mb": round(virtual_memory.used / (1024 * 1024)),
        "memory_total_mb": round(virtual_memory.total / (1024 * 1024)),
        "uptime": uptime,
        "uptime_seconds": uptime_seconds,
        "request_count": REQUEST_COUNT,
        "python_version": platform.python_version(),
        "platform": platform.system() + " " + platform.release(),
        "hostname": platform.node(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "logs": list(RECENT_LOGS)[:20]
    })

@app.get("/api/event")
def demo_event():
    """Generate a sample event to demonstrate the live log panel."""
    message = request.args.get("message", "Manual demo event")
    message = message[:160].replace("\n", " ").replace("\r", " ")
    add_event(f"DEMO EVENT: {message}")
    return jsonify({"ok": True, "message": message})

if __name__ == "__main__":
    add_event("Application starting")
    app.run(host="0.0.0.0", port=PORT, debug=False)
