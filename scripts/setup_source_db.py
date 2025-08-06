# scripts/setup_source_db.py
# Version finale : Crée la BDD source ET peuple la BDD principale avec des actualités simulées.

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DB_PATH = os.path.join(BASE_DIR, "data", "source_data.db")
MAIN_DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")

def setup_all_databases():
    """
    Prépare toutes les bases de données nécessaires au projet.
    """
    print("--- Démarrage de la configuration des bases de données ---")

    # --- 1. Création de la BDD source "legacy" ---
    print(f"Création de la base de données source à : {SOURCE_DB_PATH}")
    os.makedirs(os.path.dirname(SOURCE_DB_PATH), exist_ok=True)
    if os.path.exists(SOURCE_DB_PATH):
        os.remove(SOURCE_DB_PATH)

    conn_source = sqlite3.connect(SOURCE_DB_PATH)
    cursor_source = conn_source.cursor()
    cursor_source.execute("""
        CREATE TABLE legacy_articles (
            id INTEGER PRIMARY KEY,
            article_title TEXT NOT NULL UNIQUE,
            article_url TEXT NOT NULL
        );
    """)
    articles_to_insert = [
        ('Analyse du Halving Bitcoin 2024', 'https://example.com/halving-2024'),
        ('Les ETF Bitcoin approuvés par la SEC', 'https://example.com/etf-sec-approval'),
        ('Impact écologique du minage de Bitcoin', 'https://example.com/mining-impact')
    ]
    cursor_source.executemany("INSERT INTO legacy_articles (article_title, article_url) VALUES (?, ?)", articles_to_insert)
    conn_source.commit()
    conn_source.close()
    print("✅ Base de données source 'legacy' créée et peuplée.")

    # --- 2. Peuplement de la BDD principale avec des actualités simulées ---
    print(f"Insertion d'actualités simulées dans la base principale : {MAIN_DB_PATH}")
    
    # On s'assure que les tables existent
    from stockage import init_db
    init_db(db_path=MAIN_DB_PATH)
    
    conn_main = sqlite3.connect(MAIN_DB_PATH)
    cursor_main = conn_main.cursor()
    
    simulated_news = [
        ("Le Bitcoin dépasse un nouveau seuil historique", "https://example.com/btc-ath", "Analyse complète du nouveau record du Bitcoin."),
        ("Régulation des cryptomonnaies : Ce qui change en Europe", "https://example.com/eu-regulation", "Un aperçu des nouvelles lois MiCA."),
        ("Un grand investisseur institutionnel adopte le Bitcoin", "https://example.com/institutional-adoption", "La société X a annoncé un investissement majeur."),
        ("La technologie Lightning Network atteint 10,000 nœuds", "https://example.com/lightning-network", "Le réseau de seconde couche de Bitcoin continue sa croissance."),
        ("Comment sécuriser vos Bitcoins : Le guide complet", "https://example.com/btc-security", "Les meilleures pratiques pour protéger vos actifs numériques.")
    ]

    for title, link, content in simulated_news:
        try:
            cursor_main.execute("INSERT INTO bitcoin_news (title, link, content) VALUES (?, ?, ?)", (title, link, content))
        except sqlite3.IntegrityError:
            # L'article existe déjà, on ne fait rien
            pass
            
    conn_main.commit()
    conn_main.close()
    print("✅ Actualités simulées insérées dans la base principale.")
    print("\n--- Configuration terminée. Le système est prêt. ---")

if __name__ == "__main__":
    setup_all_databases()
