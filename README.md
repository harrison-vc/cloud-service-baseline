# cloud-service-baseline

A minimal but production-ready cloud system architecture. This repository serves as a baseline for deploying, monitoring, and troubleshooting cloud-native applications.

## Architecture Overview

- **Application**: Python (FastAPI) providing REST endpoints and health checks.
- **Server Architecture**: Designed for deployment on Linux VMs (Ubuntu/Debian) or within containers (Docker).
- **Security**: Principle of Least Privilege (POLP) applied at the service level (systemd hardening).
- **Observability**: Structured JSON logging and `/health` endpoint for external monitoring.

## Failure Domains

Understanding where things can fail is the first step to high availability.

1. **Network**: VPC peering, DNS resolution, and security group/firewall rules.
2. **Identity**: IAM role/service account permissions (S3, RDS, CloudWatch).
3. **Application**: Logic crashes, runtime exceptions, and resource leaks.
4. **Dependencies**: Upstream API failures, database connection timeouts.

## Triage Workflow (Step-by-Step)

When this application fails, follow this systematic approach:

1. **Isolate the Fault Domain**:
   - External reachability check: `curl -I http://<ip>:<port>/health`
   - Local reachability check: `curl -I http://localhost:<port>/health` (SSH required)
2. **Verify Process State**:
   - `systemctl status service-baseline` or `docker ps`
3. **Check Resource Utilization**:
   - `df -h` (Disk), `free -h` (Memory), `top` (CPU)
4. **Examine Recent Logs**:
   - `journalctl -u service-baseline -f --no-pager`

## Troubleshooting Section

- **"App Not Reachable"**: Check security group (Ingress on port 8000), VPC routing, and listener binding (`ss -tulpn`).
- **"Access Denied"**: Verify IAM role association and policy resource ARNs.
- **"App Crash"**: Investigate logs for `ModuleNotFound`, `KeyError`, or `PermissionDenied`.
- **"Timeout"**: Check upstream service status and internal worker thread availability.

## Setup Instructions

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Launch Locally**: `python app/app.py`
3. **Systemd Setup**: Copy `deploy/systemd/service-baseline.service` to `/etc/systemd/system/` and run `systemctl enable --now service-baseline`.
