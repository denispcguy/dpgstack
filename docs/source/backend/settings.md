# Django settings
Main backend configuration file at `config/settings.py`.

## Workflow: Use settings programmatically
1. Add `from django.conf import settings`.
2. Access `settings.DEBUG` or any other setting as a Python attribute.

## Common settings
- `DEBUG` — Boolean, enables debug mode. Never `True` in production.
- `DATABASES` — Database connection configuration.
- `INSTALLED_APPS` — List of enabled Django apps.
- `MIDDLEWARE` — Request/response processing pipeline.
- `TEMPLATES` — Template engine configuration, including context processors.