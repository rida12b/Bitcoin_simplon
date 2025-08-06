# Étape 1: Partir d'une image Python 3.11 officielle
FROM python:3.11-slim

# Étape 2: Installer les dépendances système pour Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libdbus-1-3 \
    libgconf-2-4 \
    libx11-xcb1 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Étape 3: Définir le répertoire de travail
WORKDIR /app

# Étape 4: Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier tout le code du projet
COPY . .