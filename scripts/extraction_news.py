import sqlite3
import os
import requests
from bs4 import BeautifulSoup

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data/bitcoin.db")
NEWS_URL = "https://bitcoinmagazine.com/news"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def setup_database():
    """Crée la base de données et la table si elles n'existent pas."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bitcoin_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("✅ Base de données prête.")

def get_news_with_requests():
    """Scrape les actualités en utilisant Requests et BeautifulSoup."""
    print("🚀 Démarrage du scraping avec Requests & BeautifulSoup...")
    articles = []
    
    try:
        print(f"🌍 Récupération de : {NEWS_URL}")
        response = requests.get(NEWS_URL, headers=HEADERS)
        response.raise_for_status()  # Lève une exception si la requête échoue
        
        print("✅ Page HTML récupérée. Analyse avec BeautifulSoup...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Sélecteur CSS pour trouver les liens des articles.
        # On cible les liens dans les titres de niveau 3 (h3) qui sont dans un conteneur d'article.
        for a_tag in soup.select('h3 a[href*="/news/"]'):
            title = a_tag.get_text(strip=True)
            link = a_tag['href']
            
            # Si le lien est relatif, on le complète
            if not link.startswith('http'):
                link = f"https://bitcoinmagazine.com{link}"

            if title:
                articles.append({
                    'title': title,
                    'link': link,
                    'content': "Contenu non récupéré."
                })

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête HTTP : {e}")
    except Exception as e:
        print(f"❌ Erreur pendant le scraping : {e}")
        
    return articles

def save_news_to_db(articles):
    """Enregistre les articles dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted_count = 0
    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO bitcoin_news (title, link, content) 
                VALUES (?, ?, ?)
            """, (article['title'], article['link'], article['content']))
            inserted_count += 1
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()
    
    if inserted_count > 0:
        print(f"💾 {inserted_count} nouveaux articles enregistrés.")
    else:
        print("✨ Aucune nouvelle actualité à ajouter.")

def main():
    """Fonction principale."""
    setup_database()
    articles = get_news_with_requests()
    
    if articles:
        print(f"\n📰 {len(articles)} articles trouvés :")
        for article in articles:
            print(f"- {article['title']}")
        save_news_to_db(articles)
    else:
        print("⚠️ Aucun article n'a pu être récupéré.")

    print("\n✅ Processus de scraping terminé.")

if __name__ == "__main__":
    main()