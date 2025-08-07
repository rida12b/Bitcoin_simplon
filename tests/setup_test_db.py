# tests/setup_test_db.py
import sqlite3
import os
import sys

# Ce script est maintenant 100% autonome et ne dépend plus de 'scripts/stockage.py'
# ce qui est une meilleure pratique pour l'isolation des tests.

# Définit le chemin de notre BDD de test
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')

def setup():
    """
    Crée et peuple une base de données de test entièrement isolée.
    """
    print(f"Préparation de la base de données de test à : {TEST_DB_PATH}")

    # Si le fichier existe, on le supprime pour repartir de zéro
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    # 1. Se connecter et CRÉER LES TABLES DIRECTEMENT ICI
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    # Création de la table des prix (copiée depuis stockage.py)
    print("Création de la table 'bitcoin_prices'...")
    cursor.execute('''
    CREATE TABLE bitcoin_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER UNIQUE,
        open REAL, high REAL, low REAL, close REAL, volume REAL
    );''')

    # Création de la table des actualités (copiée depuis stockage.py)
    print("Création de la table 'bitcoin_news'...")
    cursor.execute("""
    CREATE TABLE bitcoin_news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        content TEXT,
        timestamp DATETIME
    );""")
    print("Tables créées avec succès.")

    # 2. Insérer les données de test
    print("Insertion des données de test...")
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
