#!/usr/bin/env bash
# exit on error
set -o errexit

# Installe les dépendances système nécessaires pour Puppeteer/Chrome
apt-get update
apt-get install -y libglib2.0-0 libnss3 libdbus-1-3 libgconf-2-4 libx11-xcb1

# Installe les dépendances Python
pip install -r requirements.txt