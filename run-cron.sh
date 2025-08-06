#!/bin/bash
# exit on error
set -o errexit

echo "CRON: Lancement des migrations..."
python manage.py migrate

echo "CRON: Lancement de l'extraction des prix..."
python scripts/extraction_api.py

echo "CRON: Lancement de l'extraction des actualités..."
python scripts/extraction_news.py