# Fichier : scripts/extraction_news.py
# SOLUTION FINALE : Utilisation du flux RSS fiable de Google News.

import os
import sys
import feedparser  # La seule bibliothèque nécessaire
import sqlite3

# --- Configuration ---
# L'URL du flux RSS de Google News pour "Bitcoin" en français.
RSS_URL = "https://news.google.com/rss/search?q=Bitcoin&hl=fr&gl=FR&ceid=FR:fr"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bitcoin.db")

sys.path.append(BASE_DIR)
from scripts.stockage import init_db

def extract_news_from_rss():
    """
    Extrait les actualités depuis le flux RSS de Google News.
    C'est la méthode la plus simple et la plus fiable.
    """
    print(f"📰 Lecture du flux RSS de Google News...")
    articles = []
    
    try:
        feed = feedparser.parse(RSS_URL)

        if feed.bozo:
            # Cette erreur se produit si le flux est mal formé. Peu probable avec Google.
            print(f"❌ ERREUR : Le flux RSS est mal formé. Erreur : {feed.bozo_exception}")
            return []

        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'content': entry.get('summary', 'Aucun résumé disponible.') # Utilise .get pour plus de sécurité
            })
            
        return articles
    except Exception as e:
        print(f"❌ Une erreur critique est survenue lors de la lecture du flux RSS : {e}")
        return []

def save_news_to_db(articles):
    """Enregistre les articles extraits dans la base de données."""
    if not articles:
        return
    
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        inserted_count = 0
        for article in articles:
            try:
                cursor.execute("INSERT INTO bitcoin_news (title, link, content) VALUES (?, ?, ?)",
                               (article['title'], article['link'], article['content']))
                inserted_count += 1
            except sqlite3.IntegrityError:
                pass # L'article est un doublon, on l'ignore.
        
        conn.commit()
        if inserted_count > 0:
            print(f"💾 {inserted_count} nouveaux articles enregistrés depuis Google News.")
        else:
            print("✨ Aucune nouvelle actualité à ajouter.")
            
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde en BDD : {e}")
    finally:
        if conn:
            conn.close()

def main():
    """Fonction principale du script."""
    init_db(db_path=DB_PATH)
    articles = extract_news_from_rss()
    if articles:
        print(f"\n👍 {len(articles)} articles ont été extraits avec succès.")
        save_news_to_db(articles)
    else:
        print("\n⚠️ L'extraction n'a retourné aucun article.")
    print("\n✅ Processus de collecte d'actualités terminé.")

if __name__ == "__main__":
    main()
