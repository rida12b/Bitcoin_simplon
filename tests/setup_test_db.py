# tests/setup_test_db.py
import sqlite3
import os
import sys

# Permet d'importer depuis le dossier parent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.stockage import init_db

# Définit le chemin de notre BDD de test
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')

def setup():
    print(f"Création de la base de données de test à : {TEST_DB_PATH}")

    # Si le fichier existe, on le supprime pour repartir de zéro
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    # 1. Crée les tables dans notre BDD de test
    init_db(db_path=TEST_DB_PATH)

    # 2. Se connecte et insère des données
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    # Insère une fausse nouvelle
    cursor.execute("INSERT INTO bitcoin_news (title, link, content) VALUES (?, ?, ?)", 
                   ("Titre de test", "http://test.com", "Contenu de test"))

    # Insère 3 faux enregistrements de prix
    for i in range(3):
        cursor.execute("INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?)",
                       (1700000000 + i, 50000, 51000, 49000, 50500, 100))
    
    conn.commit()
    conn.close()
    print("Base de données de test créée et peuplée avec succès.")

if __name__ == "__main__":
    setup()