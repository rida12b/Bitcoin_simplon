# scripts/stockage.py

"""
Module de gestion du stockage des données.
Adapté pour fonctionner avec PostgreSQL (via DATABASE_URL) ou SQLite (par défaut ou via un chemin spécifié).
"""
import os
import sqlite3
import psycopg2
import psycopg2.extras
import logging

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL")
DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bitcoin.db")

def get_connection(db_path=None):
    """
    Retourne la bonne connexion de base de données.
    - En production (DATABASE_URL défini), utilise PostgreSQL.
    - En local/test, utilise SQLite. Si un db_path est fourni, il l'utilise, sinon il prend le chemin par défaut.
    """
    if DATABASE_URL and "sqlite" not in DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        # Gère le cas où DATABASE_URL est une URL SQLite (pour les tests) ou n'est pas défini.
        path_to_use = db_path
        if not path_to_use:
            if DATABASE_URL:
                path_to_use = DATABASE_URL.split('sqlite:///')[-1]
            else:
                path_to_use = DEFAULT_SQLITE_PATH
        
        os.makedirs(os.path.dirname(path_to_use), exist_ok=True)
        return sqlite3.connect(path_to_use)

def init_db(db_path=None):
    """Initialise la BDD au chemin spécifié et crée les tables si elles n'existent pas."""
    conn = None
    try:
        # On passe le chemin à la fonction de connexion.
        conn = get_connection(db_path=db_path)
        cursor = conn.cursor()
        
        if isinstance(conn, psycopg2.extensions.connection): # PostgreSQL
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id SERIAL PRIMARY KEY, timestamp BIGINT UNIQUE,
                open REAL, high REAL, low REAL, close REAL, volume REAL
            );''')
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_news (
                id SERIAL PRIMARY KEY, title TEXT NOT NULL UNIQUE,
                link TEXT NOT NULL, content TEXT, timestamp TIMESTAMPTZ
            );""")
        else: # SQLite
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER UNIQUE,
                open REAL, high REAL, low REAL, close REAL, volume REAL
            );''')
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE,
                link TEXT NOT NULL, content TEXT, timestamp DATETIME
            );""")

        conn.commit()
        logging.info(f"Initialisation de la base de données à '{db_path or 'default'}' terminée.")
    except Exception as e:
        logging.error(f"Erreur lors de l'initialisation de la BDD : {e}")
    finally:
        if conn:
            conn.close()

def insert_many_prices(data_list, db_path=None):
    """Insère plusieurs lignes dans la table `bitcoin_prices` dans la BDD spécifiée."""
    if not data_list:
        return

    conn = None
    try:
        conn = get_connection(db_path=db_path)
        cursor = conn.cursor()
        
        to_insert = [(d['timestamp'], d['open'], d['high'], d['low'], d['close'], d['volume']) for d in data_list]
        
        if isinstance(conn, psycopg2.extensions.connection): # PostgreSQL
            sql = "INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (timestamp) DO NOTHING;"
            psycopg2.extras.execute_batch(cursor, sql, to_insert)
        else: # SQLite
            sql = "INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?);"
            cursor.executemany(sql, to_insert)
        
        conn.commit()
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion des prix : {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

# Ajout du logger pour éviter les erreurs si le module est importé
logging.basicConfig(level=logging.INFO)
