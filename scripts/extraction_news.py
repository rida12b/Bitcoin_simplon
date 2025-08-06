import os
import sys
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# Charger les variables d'environnement (notamment DATABASE_URL)
load_dotenv()

# --- Configuration ---
DATABASE_URL = os.environ.get('DATABASE_URL')
TARGET_URL = "https://news.bitcoin.com/"

def extract_news_with_browser():
    """
    Pilote un navigateur Chrome pour scraper les données d'un site dynamique.
    """
    print(f"🚀 Démarrage du navigateur pour scraper : {TARGET_URL}...")
    articles = []
    
    options = uc.ChromeOptions()
    # Options nécessaires pour fonctionner dans un environnement Docker/headless
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None # Initialiser driver à None
    try:
        driver = uc.Chrome(options=options)
        driver.get(TARGET_URL)
        print("⏳ Attente de 10 secondes pour le chargement du contenu par JavaScript...")
        time.sleep(10)

        print("✅ Contenu chargé. Récupération du code HTML final...")
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        article_containers = soup.select("div.article-card")

        if not article_containers:
            print("❌ ERREUR : Aucun article trouvé avec le sélecteur 'div.article-card'.")
            return []
            
        print(f"📰 {len(article_containers)} articles potentiels détectés.")

        for container in article_containers:
            title_tag = container.select_one("h5.article-card__title")
            link_tag = container.find('a', href=True)

            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag.get('href')
                if not link.startswith('http'):
                    link = f"https://news.bitcoin.com{link}"

                articles.append({
                    'title': title,
                    'link': link,
                    'content': "Contenu non récupéré."
                })
        
        return [art for art in articles if art.get('title')]

    except Exception as e:
        print(f"❌ Une erreur est survenue pendant l'automatisation du navigateur : {e}")
        return []
    finally:
        if driver:
            print("🚪 Fermeture du navigateur.")
            driver.quit()

def save_news_to_db(articles):
    """Enregistre les articles dans la base de données PostgreSQL."""
    if not articles:
        print("Aucun article à enregistrer.")
        return
        
    if not DATABASE_URL:
        print("Erreur: La variable d'environnement DATABASE_URL n'est pas configurée.")
        return

    to_insert = [(art['title'], art['link'], art['content']) for art in articles]
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # Utilise ON CONFLICT pour ignorer les doublons de manière efficace
                extras.execute_values(
                    cursor,
                    "INSERT INTO bitcoin_news (title, link, content) VALUES %s ON CONFLICT (title) DO NOTHING",
                    to_insert
                )
        print(f"💾 {cursor.rowcount} nouvelles actualités insérées.")
    except Exception as e:
        print(f"❌ Erreur de base de données (News): {e}")

if __name__ == "__main__":
    articles = extract_news_with_browser()
    if articles:
        print(f"\n👍 {len(articles)} articles ont été extraits avec succès.")
        save_news_to_db(articles)
    else:
        print("⚠️ L'extraction n'a retourné aucun article.")
    print("\n✅ Processus de scraping terminé.")