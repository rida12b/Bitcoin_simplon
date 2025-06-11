"""
Module de gestion du stockage des prix du Bitcoin dans une base SQLite.
Fournit des fonctions pour initialiser la base, insérer une ou plusieurs lignes.
"""

import sqlite3
import os

DB_FILENAME = "bitcoin_data.db"

def init_db():
    """
    Initialise la base de données et crée la table bitcoin_prices si elle n'existe pas.
    """
    conn = sqlite3.connect(DB_FILENAME)
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

    conn.commit()
    conn.close()

def insert_data(timestamp, open, high, low, close, volume):
    """
    Insère une ligne dans la table bitcoin_prices.
    Ignore l'insertion si le timestamp existe déjà (unicité).
    """
    conn = sqlite3.connect(DB_FILENAME)
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
    conn = sqlite3.connect(DB_FILENAME)
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