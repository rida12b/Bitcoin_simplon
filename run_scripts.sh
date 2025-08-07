#!/bin/bash

# Définit le chemin vers l'exécutable Python du venv
PYTHON_EXEC="/root/Bitcoin_simplon/venv/bin/python"

# Définit le chemin vers le répertoire du projet
PROJECT_DIR="/root/Bitcoin_simplon"

echo "--- Tâche Cron démarrée le $(date) ---"

echo "Lancement du script d'extraction des prix depuis l'API..."
$PYTHON_EXEC "$PROJECT_DIR/scripts/extraction_api.py"

echo "Lancement du script d'extraction des actualités depuis le FLUX RSS..."
$PYTHON_EXEC "$PROJECT_DIR/scripts/extraction_news.py"

echo "Lancement du script d'extraction depuis la source SQL..."
$PYTHON_EXEC "$PROJECT_DIR/scripts/extraction_sql.py"

echo "Tâches de collecte terminées."
echo "--- Tâche Cron terminée le $(date) ---"