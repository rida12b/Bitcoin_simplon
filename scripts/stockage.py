"""
Module de gestion du stockage des données.
Adapté pour fonctionner avec PostgreSQL (via DATABASE_URL) ou SQLite (par défaut).
"""
import os
import sqlite3
import psycopg2
import psycopg2.extras # Important pour l'insertion en masse

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL")
DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bitcoin.db")

def get_connection():
    """Retourne la bonne connexion de base de données en fonction de l'environnement."""
    if DATABASE_URL:
        # Mode Production: utilise PostgreSQL
        print("INFO (stockage): Utilisation de la connexion PostgreSQL.")
        return psycopg2.connect(DATABASE_URL)
    else:
        # Mode Local/Test: utilise SQLite
        print("INFO (stockage): Utilisation de la base de données SQLite.")
        os.makedirs(os.path.dirname(DEFAULT_SQLITE_PATH), exist_ok=True)
        return sqlite3.connect(DEFAULT_SQLITE_PATH)

def init_db():
    """Initialise la base de données et crée les tables si elles n'existent pas."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # La syntaxe de création est légèrement différente (SERIAL vs AUTOINCREMENT)
        if isinstance(conn, psycopg2.extensions.connection): # C'est PostgreSQL
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id SERIAL PRIMARY KEY,
                timestamp BIGINT UNIQUE,
                open REAL, high REAL, low REAL, close REAL, volume REAL
            );''')
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_news (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                link TEXT NOT NULL,
                content TEXT,
                timestamp TIMESTAMPTZ
            );""")
        else: # C'est SQLite
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bitcoin_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER UNIQUE,
                open REAL, high REAL, low REAL, close REAL, volume REAL
            );''')
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                link TEXT NOT NULL,
                content TEXT,
                timestamp DATETIME
            );""")

        conn.commit()
        print("INFO (stockage): Initialisation de la base de données terminée.")
    except Exception as e:
        print(f"ERREUR (stockage.init_db): {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

def insert_many_prices(data_list):
    """Insère plusieurs lignes dans la table `bitcoin_prices`."""
    if not data_list:
        print("WARNING (stockage): Aucune donnée de prix à insérer.")
        return

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        to_insert = [(d['timestamp'], d['open'], d['high'], d['low'], d['close'], d['volume']) for d in data_list]
        
        if isinstance(conn, psycopg2.extensions.connection): # C'est PostgreSQL
            # Syntaxe PostgreSQL pour ignorer les doublons
            sql = """
                INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
            """
            psycopg2.extras.execute_batch(cursor, sql, to_insert)
        else: # C'est SQLite
            # Syntaxe SQLite pour ignorer les doublons
            sql = """
                INSERT OR IGNORE INTO bitcoin_prices (timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            cursor.executemany(sql, to_insert)
        
        # Le commit est absolument CRUCIAL pour PostgreSQL
        conn.commit()
        print(f"INFO (stockage): Tentative d'insertion de {len(to_insert)} lignes. {cursor.rowcount} lignes affectées.")
        
    except Exception as e:
        print(f"ERREUR (stockage.insert_many_prices): Échec de l'insertion. Erreur: {e}")
        if conn:
            conn.rollback() # Annule la transaction en cas d'erreur
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db()
