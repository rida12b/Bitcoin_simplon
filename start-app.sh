#!/bin/bash
# exit on error
set -o errexit

# On lance les migrations de la base de données
python manage.py migrate

# On lance le serveur Gunicorn
gunicorn dashboard.wsgi:application --bind 0.0.0.0:${PORT:-8000}