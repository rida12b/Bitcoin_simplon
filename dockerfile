# Étape 1: Partir d'une image Python officielle et légère
# python:3.11-slim est une bonne base car elle est optimisée en taille.
FROM python:3.11-slim

# Étape 2: Définir le répertoire de travail à l'intérieur du conteneur
# Toutes les commandes suivantes s'exécuteront à partir de ce dossier.
WORKDIR /app

# Étape 3: Copier uniquement le fichier des dépendances pour optimiser le cache Docker
# Si requirements.txt ne change pas, Docker n'aura pas à réinstaller les dépendances à chaque build.
COPY requirements.txt .

# Étape 4: Installer les dépendances
# --no-cache-dir réduit la taille finale de l'image.
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier tout le reste du code du projet dans le conteneur
COPY . .

# Étape 6: Exposer le port que l'API utilisera à l'intérieur du conteneur
# Cela indique à Docker que l'application écoutera sur le port 8001.
EXPOSE 8001

# Étape 7: La commande à exécuter au démarrage du conteneur
# Lance le serveur Uvicorn, en le rendant accessible de l'extérieur du conteneur (--host 0.0.0.0).
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"]