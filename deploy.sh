#!/bin/bash
set -e # Arrête le script si une commande échoue

echo "🚀 Démarrage du déploiement..."

# 1. Assurer que nous sommes bien sur la branche main
git checkout main

# 2. Récupérer toutes les dernières informations de GitHub sans rien modifier
git fetch origin

# 3. Forcer la branche locale à être identique à celle de GitHub
# C'est la commande clé qui résout le problème des branches divergentes
git reset --hard origin/main
echo "✅ Code source synchronisé de force avec GitHub."

# 4. Activer l'environnement virtuel et installer les dépendances
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Dépendances installées/mises à jour."

# 5. Redémarrer les services pour appliquer les changements
echo "🔄 Redémarrage des services Gunicorn..."
sudo systemctl restart gunicorn_api
sudo systemctl restart gunicorn_django
echo "✅ Services redémarrés avec succès."

echo "🎉 Déploiement terminé !"
