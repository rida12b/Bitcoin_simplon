#!/bin/bash

echo "Initialisation de la base de données (si nécessaire)..."
python manage.py migrate

echo "Lancement du script d'extraction des prix depuis l'API..."
python scripts/extraction_api.py

echo "Lancement du script d'extraction des actualités depuis le FLUX RSS..."
python scripts/extraction_news.py

echo "Lancement du script d'extraction depuis la source SQL..."
python scripts/extraction_sql.py

echo "Tâches de collecte terminées."
