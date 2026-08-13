#!/usr/bin/env bash
set -o errexit

python manage.py migrate --no-input
python manage.py load_catalog_if_empty

exec gunicorn aura.wsgi:application --bind "0.0.0.0:${PORT:-10000}"
