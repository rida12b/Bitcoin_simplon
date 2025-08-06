import os
import feedparser
from dotenv import load_dotenv
# MODIFIÉ : Importe les nouvelles fonctions
from stockage import init_db, insert_many_news

load_dotenv()

RSS_URL = "https://news.google.com/rss/search?q=Bitcoin&hl=fr&gl=FR&ceid=FR:fr"

def extract_news_from_rss():
    print("Lancement de l'extraction des actualités depuis le FLUX RSS...")
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.bozo:
            print(f"❌ ERREUR : Le flux RSS est mal formé : {feed.bozo_exception}")
            return []
        
        return [{
            'title': entry.title, 'link': entry.link,
            'content': entry.get('summary', 'Aucun résumé disponible.')
        } for entry in feed.entries]
    except Exception as e:
        print(f"❌ Erreur critique lors de la lecture du flux RSS : {e}")
        return []

if __name__ == "__main__":
    init_db()
    articles = extract_news_from_rss()
    if articles:
        # MODIFIÉ : Appelle la fonction spécifique aux actualités
        insert_many_news(articles)
    else:
        print("🟡 Aucune actualité extraite du flux RSS.")
