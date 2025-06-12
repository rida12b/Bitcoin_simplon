"""
Module de gestion du stockage des prix du Bitcoin dans une base SQLite.
Fournit des fonctions pour initialiser la base, insérer une ou plusieurs lignes.
"""

import sqlite3
import os

# Correction du chemin pour pointer vers le dossier /data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")

def init_db():
    """
    Initialise la base de données et crée la table bitcoin_prices si elle n'existe pas.
    """
    # S'assurer que le dossier /data existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER UNIQUE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL
    )
    ''')

    # Ajout de la création de la table des news pour unifier l'initialisation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bitcoin_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL,
            content TEXT,
            timestamp DATETIME
        );
    """)

    conn.commit()
    conn.close()

def insert_data(timestamp, open, high, low, close, volume):
    """
    Insère une ligne dans la table bitcoin_prices.
    Ignore l'insertion si le timestamp existe déjà (unicité).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, open, high, low, close, volume))
    conn.commit()
    conn.close()

def insert_many(data_list):
    """
    Insère plusieurs lignes dans la table bitcoin_prices à partir d'une liste de dictionnaires.
    Ignore les doublons sur le timestamp.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (d['timestamp'], d['open'], d['high'], d['low'], d['close'], d['volume'])
        for d in data_list
    ])
    conn.commit()
    conn.close()