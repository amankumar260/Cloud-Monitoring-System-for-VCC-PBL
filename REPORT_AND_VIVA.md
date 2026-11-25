# Project Report and Viva Notes
## Title
**Python-Based Cloud Application Monitoring System (No Docker)**

## Abstract
This project implements a local web-based monitoring dashboard using Python and Flask. It displays CPU and memory statistics available through psutil, application uptime, request count, runtime details, and recent events. JSON endpoints provide application health and metrics. The application is run directly from VS Code without Docker or a cloud account. It is a lightweight educational prototype for application monitoring and cloud programming concepts.

## Problem statement
A developer needs a simple way to check whether a web application is responding and to inspect basic runtime statistics without relying on a separate monitoring platform.

## Objectives
1. Develop a monitoring dashboard using Python and Flask.
2. Expose health and metrics through HTTP endpoints.
3. Display CPU, memory, uptime, request count and recent events.
4. Run and test the application locally without Docker.
5. Explain how the design could later be deployed on a VM or cloud platform.

## Technologies
- Python: main programming language.
- Flask: web framework.
- psutil: system and CPU/memory metrics.
- HTML/CSS/JavaScript: dashboard interface.
- unittest: automated endpoint tests.

## Architecture
Browser -> local Flask server -> dashboard/API routes -> psutil metrics and in-memory event log.

## Modules
- Dashboard: renders the monitoring interface.
- Health endpoint: `/health`.
- Metrics endpoint: `/api/metrics`.
- Demo event endpoint: `/api/event?message=...`.
- Test module: checks the main routes and expected JSON fields.

## Testing plan

| Test case | Expected result |
|---|---|
| Open dashboard `/` | HTTP 200 and dashboard HTML |
| Open `/health` | HTTP 200 and status `healthy` |
| Open `/api/metrics` | JSON includes CPU, memory, uptime, request count and logs |
| Trigger `/api/event` | JSON confirms event recorded |
| Run unittest discovery | Four tests pass |

Only record tests as passed after running them. Add screenshots of the actual dashboard and endpoints to the final report.

## Limitations
- Local-only application; no public cloud deployment.
- No Docker, hypervisor, or VM provisioning.
- Recent events are kept in memory and reset when the process restarts.
- No login, TLS, historical database, alerting or multi-server monitoring.

## Future scope
- Deploy on a Linux virtual machine.
- Add login and role-based access.
- Store metrics and logs in a database.
- Add historical charts and threshold alerts.
- Optionally containerize the app later.

## Conclusion
The project demonstrates a simple Python monitoring web application with health and metrics endpoints. It can be run quickly on a local computer and provides a base for later cloud deployment. It should be described accurately as a local application-monitoring prototype, not as a live cloud or virtualization platform.

## Viva questions and answers

**1. What is cloud computing?**  
On-demand access to computing resources such as servers, storage, networking and software over a network.

**2. What is virtualization?**  
Abstraction of physical computing resources to create isolated virtual environments.

**3. Does this project use Docker?**  
No. This version runs directly through Python and Flask.

**4. Does this project create a virtual machine?**  
No. It monitors the local runtime; VM creation would require a hypervisor or cloud-provider API.

**5. What is Flask?**  
A lightweight Python web framework for defining routes and returning web pages or JSON.

**6. What is psutil?**  
A Python library for accessing system and process information, including CPU and memory statistics.

**7. What is an API endpoint?**  
A URL through which a client accesses a defined application operation.

**8. What does `/health` do?**  
It returns a simple healthy status if the application is responding.

**9. What does `/api/metrics` return?**  
JSON containing runtime metrics such as CPU, memory, uptime, request count and recent events.

**10. What is monitoring?**  
Collecting and presenting information about system or application state to help detect problems.

**11. What is high availability?**  
Designing a service to minimize downtime through redundancy and recovery mechanisms. This prototype does not implement full high availability.

**12. How could it be deployed to a cloud?**  
Run it on a cloud VM, configure networking and a process manager, and add HTTPS, authentication and firewall rules.

**13. What are IaaS, PaaS and SaaS?**  
IaaS provides infrastructure, PaaS provides a managed application platform, and SaaS delivers ready-to-use software.

**14. What are the limitations?**  
Local-only operation, in-memory logs, no authentication, no long-term storage and no cloud-provider integration.

**15. What would you improve next?**  
Add persistent metrics, alerts, access control, historical charts and deployment on a virtual machine.
