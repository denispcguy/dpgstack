# Monitoring
Dpgstack includes Prometheus metrics and Grafana dashboards for production monitoring:
- **Prometheus**: Scrapes metrics from the Django app via `/metrics` endpoint
- **Grafana**: Pre-configured dashboards for request latency, error rates, and huey task status
- **Notifications**: Push notifications via webpush for critical errors

Key metrics tracked: request count, response times, database query count, huey task queue depth.
