#!/bin/sh
set -e

uv run manage.py migrate --noinput
DJANGO_SUPERUSER_PASSWORD=1 uv run python manage.py createsuperuser --noinput --username admin --email admin@example.com

exec uv run gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 12 \
    --timeout 180
