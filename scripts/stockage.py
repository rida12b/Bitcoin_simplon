"""
Module de gestion du stockage des données dans une base SQLite.
Fournit des fonctions pour initialiser la base et insérer des données.
Les fonctions sont flexibles et peuvent accepter un chemin de base de données
spécifique, ce qui est utile pour les tests.
"""
import sqlite3
import os

# --- Configuration des Chemins ---
# Ce chemin est utilisé par défaut si aucun autre n'est spécifié.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")


# --- Fonctions de Gestion de la Base de Données ---

def init_db(db_path=DB_PATH):
    """
    Initialise la base de données au chemin spécifié et crée les tables
    `bitcoin_prices` et `bitcoin_news` si elles n'existent pas.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Création de la table pour les prix
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER UNIQUE,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )''')

    # Création de la table pour les actualités
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bitcoin_news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        content TEXT,
        timestamp DATETIME
    )""")

    conn.commit()
    conn.close()


def insert_data(timestamp, open, high, low, close, volume, db_path=DB_PATH):
    """
    Insère une seule ligne dans la table `bitcoin_prices` de la BDD spécifiée.
    Ignore l'insertion si le timestamp existe déjà (grâce à la contrainte UNIQUE).
    """
    conn = sqlite3.connect(db_path) # Utilise le chemin fourni
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, open, high, low, close, volume))
    conn.commit()
    conn.close()


def insert_many(data_list, db_path=DB_PATH):
    """
    Insère plusieurs lignes dans la table `bitcoin_prices` de la BDD spécifiée.
    Ignore les doublons basés sur le timestamp.
    """
    conn = sqlite3.connect(db_path) # Utilise le chemin fourni
    cursor = conn.cursor()
    
    # Prépare les données pour l'insertion en masse
    to_insert = [
        (d['timestamp'], d['open'], d['high'], d['low'], d['close'], d['volume'])
        for d in data_list
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', to_insert)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Initialisation de la base de données principale...")
    # Appelle la fonction pour créer les tables si elles n'existent pas.
    init_db()
    print("✅ Base de données principale initialisée avec succès.")