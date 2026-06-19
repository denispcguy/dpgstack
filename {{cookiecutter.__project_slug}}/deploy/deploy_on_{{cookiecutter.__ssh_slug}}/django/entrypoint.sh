#!/bin/sh
set -e

uv run manage.py migrate --noinput
uv run manage.py populate

exec uv run gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 12 \
    --timeout 180
