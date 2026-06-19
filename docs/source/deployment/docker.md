# Docker
Dpgstack uses Docker for containerized deployment. The `deploy/deploy_on_localhost/` directory contains a compose setup with:
- Django/Gunicorn application
- NGINX reverse proxy
- PostgreSQL database
- Prometheus for metrics
- Grafana for dashboards

Build and run with `docker compose up -d` from the deploy directory.
