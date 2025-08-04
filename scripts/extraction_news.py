# Fichier : scripts/extraction_news.py
# Version finale utilisant les sélecteurs CSS exacts, trouvés grâce au fichier debug_page.html.

import os
import sys
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import sqlite3


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bitcoin.db")
print(f"CHEMIN DB (SCRIPT): {os.path.abspath(DB_PATH)}") # <---

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.stockage import init_db

# --- Configuration ---
TARGET_URL = "https://news.bitcoin.com/"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bitcoin.db")

def extract_news_with_browser():
    """
    Pilote un vrai navigateur et utilise les sélecteurs CSS corrects pour extraire les données.
    """
    print(f"🚀 Démarrage du navigateur pour scraper : {TARGET_URL}...")
    articles = []
    
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # À activer pour ne plus voir le navigateur
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(TARGET_URL)
        print("⏳ Attente de 5 secondes pour le chargement du contenu par JavaScript...")
        time.sleep(5)

        print("✅ Contenu chargé. Récupération du code HTML final...")
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- LE SÉLECTEUR FINAL ET CORRECT ---
        # D'après debug_page.html, chaque article est dans une div avec la classe "sc-dDSDPK".
        article_containers = soup.select("div.sc-dDSDPK")

        if not article_containers:
            print("❌ ERREUR : Aucun article trouvé avec le sélecteur 'div.sc-dDSDPK'.")
            return []
            
        print(f"📰 {len(article_containers)} articles potentiels détectés.")

        for container in article_containers:
            # À l'intérieur de chaque conteneur, le titre est dans un <h6>
            title_tag = container.select_one("h6")
            # Le lien est sur la balise <a> parente
            link_tag = container.find('a', href=True)

            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                # Le lien peut être relatif, on le reconstruit
                link = link_tag.get('href')
                if not link.startswith('http'):
                    link = f"https://news.bitcoin.com{link}"

                articles.append({
                    'title': title,
                    'link': link,
                    'content': "Contenu non récupéré." # La description n'est pas sur la page principale
                })
        
        # On ne garde que les articles qui ont un titre (pour filtrer les conteneurs vides)
        articles = [art for art in articles if art.get('title')]
        return articles

    except Exception as e:
        print(f"❌ Une erreur est survenue pendant l'automatisation du navigateur : {e}")
        return []
    finally:
        print("🚪 Fermeture du navigateur.")
        driver.quit()

def save_news_to_db(articles):
    """Enregistre les articles dans la base de données."""
    if not articles: return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted_count = 0
    for article in articles:
        try:
            cursor.execute("INSERT INTO bitcoin_news (title, link, content) VALUES (?, ?, ?)",
                           (article['title'], article['link'], article['content']))
            inserted_count += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    if inserted_count > 0: print(f"💾 {inserted_count} nouveaux articles enregistrés.")
    else: print("✨ Aucune nouvelle actualité à ajouter.")

def main():
    """Fonction principale."""
    init_db(db_path=DB_PATH)
    articles = extract_news_with_browser()
    if articles:
        print(f"\n👍 {len(articles)} articles ont été extraits avec succès.")
        save_news_to_db(articles)
    else:
        print("⚠️ L'extraction n'a retourné aucun article.")
    print("\n✅ Processus de scraping terminé.")

if __name__ == "__main__":
    main()