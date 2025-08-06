"""
Module de gestion du stockage.
Peut se connecter à PostgreSQL (via DATABASE_URL) ou à SQLite.
"""
import os
import sys
import sqlite3
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Charger les variables d'environnement (pour DATABASE_URL)
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
IS_POSTGRES = DATABASE_URL is not None

# Chemin par défaut pour SQLite (utilisé si DATABASE_URL n'est pas définie)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")

def get_db_connection():
    """Retourne une connexion à la BDD appropriée."""
    if IS_POSTGRES:
        return psycopg2.connect(DATABASE_URL)
    else:
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        return sqlite3.connect(SQLITE_DB_PATH)

def init_db():
    """Crée les tables si elles n'existent pas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql_create_prices = """
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        id SERIAL PRIMARY KEY,
        timestamp BIGINT UNIQUE,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    );
    """
    
    sql_create_news = """
    CREATE TABLE IF NOT EXISTS bitcoin_news (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        content TEXT,
        timestamp TIMESTAMPTZ
    );
    """
    
    # Adapte la syntaxe pour SQLite si besoin
    if not IS_POSTGRES:
        sql_create_prices = sql_create_prices.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT").replace("BIGINT", "INTEGER")
        sql_create_news = sql_create_news.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT").replace("TIMESTAMPTZ", "DATETIME")

    cursor.execute(sql_create_prices)
    cursor.execute(sql_create_news)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables de la base de données initialisées (si nécessaire).")


def insert_many_prices(data_list):
    """Insère plusieurs lignes dans la table bitcoin_prices."""
    if not data_list:
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (timestamp) DO NOTHING;
    """
    
    if not IS_POSTGRES:
        query = query.replace("%s", "?").replace("ON CONFLICT (timestamp) DO NOTHING", "OR IGNORE")

    to_insert = [
        (d['timestamp'], d['open'], d['high'], d['low'], d['close'], d['volume'])
        for d in data_list
    ]
    
    cursor.executemany(query, to_insert)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"💾 {len(to_insert)} lignes de prix traitées.")


def insert_many_news(articles):
    """Insère plusieurs articles dans la table bitcoin_news."""
    if not articles:
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO bitcoin_news (title, link, content)
    VALUES (%s, %s, %s)
    ON CONFLICT (title) DO NOTHING;
    """
    
    if not IS_POSTGRES:
        query = query.replace("%s", "?").replace("ON CONFLICT (title) DO NOTHING", "OR IGNORE")

    to_insert = [(art['title'], art['link'], art['content']) for art in articles]
    
    cursor.executemany(query, to_insert)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"💾 {len(to_insert)} articles traités.")
