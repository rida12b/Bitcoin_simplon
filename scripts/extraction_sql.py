import sqlite3
import os
import sys

# Assurer que le module 'stockage' peut être importé
# (peut être redondant si votre structure est déjà bien configurée, mais c'est une bonne pratique)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DB_PATH = os.path.join(BASE_DIR, "data", "source_data.db")
DESTINATION_DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")

def extract_from_sql_source():
    """
    Se connecte à la base de données source, extrait les articles
    en utilisant une requête SQL, et les insère dans la base de données principale.
    """
    print("🚀 Démarrage de l'extraction depuis la source SQL...")

    try:
        # --- Connexion à la base de données SOURCE ---
        source_conn = sqlite3.connect(SOURCE_DB_PATH)
        source_cursor = source_conn.cursor()

        # --- ÉTAPE CLÉ : La requête SQL pour extraire les données (Compétence C2) ---
        print("Exécution de la requête SELECT sur la base source...")
        query = "SELECT article_title, article_url FROM legacy_articles;"
        source_cursor.execute(query)
        articles_from_source = source_cursor.fetchall()
        
        # Fermer la connexion à la source une fois les données récupérées
        source_conn.close()

        if not articles_from_source:
            print("🟡 Aucune nouvelle donnée à extraire de la source SQL.")
            return

        print(f"✅ {len(articles_from_source)} articles extraits de la source.")
        
        # --- Formatage des données pour la base de destination ---
        formatted_articles = [
            {
                'title': row[0],
                'link': row[1],
                'content': 'Contenu extrait depuis la base de données interne.' # Contenu générique
            }
            for row in articles_from_source
        ]

        # --- Connexion à la base de données de DESTINATION ---
        dest_conn = sqlite3.connect(DESTINATION_DB_PATH)
        dest_cursor = dest_conn.cursor()

        # --- Insertion dans la table bitcoin_news ---
        print("Insertion des données formatées dans la base de destination...")
        inserted_count = 0
        for article in formatted_articles:
            try:
                dest_cursor.execute(
                    "INSERT INTO bitcoin_news (title, link, content) VALUES (?, ?, ?)",
                    (article['title'], article['link'], article['content'])
                )
                inserted_count += 1
            except sqlite3.IntegrityError:
                # Gère le cas où l'article existe déjà (grâce à la contrainte UNIQUE)
                pass
        
        dest_conn.commit()
        dest_conn.close()
        
        if inserted_count > 0:
            print(f"💾 {inserted_count} nouveaux articles insérés dans la base principale.")
        else:
            print("✨ Aucun nouvel article à ajouter (déjà présents).")

    except sqlite3.OperationalError as e:
        print(f"❌ Erreur de base de données : {e}")
        print("Veuillez vous assurer que la base de données source a été créée avec 'python scripts/setup_source_db.py'")

if __name__ == "__main__":
    extract_from_sql_source()