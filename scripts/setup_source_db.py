import sqlite3
import os

# --- Configuration ---
# Définit le chemin de notre BDD "source"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DB_PATH = os.path.join(BASE_DIR, "data", "source_data.db")
NEWS_TABLE_NAME = "legacy_articles"

def create_source_database():
    """
    Crée une fausse base de données 'source' pour simuler un système existant.
    Cette base de données contient des articles à extraire.
    """
    print(f"Création de la base de données source à : {SOURCE_DB_PATH}")

    # S'assurer que le dossier /data existe
    os.makedirs(os.path.dirname(SOURCE_DB_PATH), exist_ok=True)

    # Supprimer l'ancienne base si elle existe pour un départ propre
    if os.path.exists(SOURCE_DB_PATH):
        os.remove(SOURCE_DB_PATH)

    # Se connecter (crée le fichier si non existant) et obtenir un curseur
    conn = sqlite3.connect(SOURCE_DB_PATH)
    cursor = conn.cursor()

    # Créer la table des articles "legacy"
    print(f"Création de la table '{NEWS_TABLE_NAME}'...")
    cursor.execute(f"""
        CREATE TABLE {NEWS_TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_title TEXT NOT NULL UNIQUE,
            article_url TEXT NOT NULL,
            publication_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Insérer quelques fausses données
    print("Insertion de données de test dans la source...")
    articles_to_insert = [
        ('Analyse du Halving Bitcoin 2024', 'https://example.com/halving-2024'),
        ('Les ETF Bitcoin approuvés par la SEC', 'https://example.com/etf-sec-approval'),
        ('Impact écologique du minage de Bitcoin', 'https://example.com/mining-impact')
    ]

    cursor.executemany(f"""
        INSERT INTO {NEWS_TABLE_NAME} (article_title, article_url)
        VALUES (?, ?)
    """, articles_to_insert)

    # Valider les changements et fermer la connexion
    conn.commit()
    conn.close()

    print("✅ Base de données source créée et peuplée avec succès.")

if __name__ == "__main__":
    create_source_database()