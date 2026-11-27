Cloud Deployment and Monitoring System — No Docker Version

**Subject:** Virtualisation and Cloud Computing  
**Stack:** Python, Flask, psutil, HTML/CSS/JavaScript  
**Run mode:** Directly in VS Code; no Docker required

## Features
- Live CPU and memory usage reported by `psutil`
- Application uptime and request counter
- Runtime/platform details
- Health endpoint and JSON metrics endpoint
- Recent application events
- Dashboard refreshes automatically every five seconds

Requirements
- Python 3.10+ recommended
- VS Code
- Internet connection for the first installation of Python packages

## Windows setup (VS Code terminal)

Open this folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

If installation succeeds, open these URLs in your browser:

- Dashboard: http://127.0.0.1:5000
- Health check: http://127.0.0.1:5000/health
- JSON metrics: http://127.0.0.1:5000/api/metrics
- Demo event: http://127.0.0.1:5000/api/event?message=Hello%20examiner

Keep the terminal open while demonstrating the application. Press `Ctrl+C` to stop it.

 macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```
Automated tests

After installing dependencies, open a second terminal in the project folder and run:

```bash
python -m unittest discover -s tests -v
```

On Windows, if `python` is not available, use:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Troubleshooting
- **`py` not found:** Install Python from python.org and select the option to add Python to PATH, then reopen VS Code.
- **Port 5000 is busy:** In PowerShell, run `$env:PORT="5001"; .\.venv\Scripts\python.exe app.py`, then open `http://127.0.0.1:5001`.
- **Package install fails:** Check internet access and run the pip install command again.
- **Dashboard fails to load:** Check the terminal for errors and confirm the server says it is running on port 5000.
- **Metrics:** This version runs directly on your computer, so `psutil` generally reports host OS statistics rather than container-specific metrics.

## Architecture

```text
Browser
  |
  | HTTP requests to 127.0.0.1:5000
  v
Flask application (app.py)
  |-- Dashboard HTML/CSS/JavaScript
  |-- /health       -> health JSON
  |-- /api/metrics  -> CPU, memory, uptime, requests and recent logs
  |-- /api/event    -> adds a sample event
  |
  +--> psutil reads runtime/system metrics
```

## Syllabus mapping and honest project scope

| Syllabus area | Demonstration |
|---|---|
| Cloud programming environment | Python web application and HTTP endpoints |
| Monitoring and reliability | Health endpoint, uptime, status and event log |
| Cloud application deployment concepts | Running a web service in a repeatable Python environment |
| Virtualization concepts | Discuss how this app could be packaged into a container or deployed on a VM |

**Scope note:** This no-Docker version is a local monitoring application. It does not itself create virtual machines, use a hypervisor, or deploy to a public cloud. Explain virtualization and cloud deployment as concepts and future extensions; do not claim that this local version demonstrates containerization.

## Suggested demo
1. Start the app in VS Code.
2. Open the dashboard and show live CPU/memory metrics.
3. Open `/health` and `/api/metrics`.
4. Open `/api/event?message=Live%20demo` and show the event in the dashboard.
5. Run automated tests in a second terminal.
6. Capture screenshots for your report.
