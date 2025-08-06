import logging
import os
import sys
from fastapi import FastAPI, HTTPException, Depends
import psycopg2
import psycopg2.extras  # Important pour avoir des résultats sous forme de dictionnaire

# --- Configuration du Path ---
# Ajoute le dossier parent au path pour trouver le module 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.llm_analyzer import analyze_text

# --- Configuration de la Journalisation ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - API - %(message)s'
)

# --- Initialisation de l'Application FastAPI ---
app = FastAPI(
    title="Bitcoin Analyzer API",
    description="Une API pour récupérer les données et analyses sur le Bitcoin.",
    version="1.0.0"
)

# --- Gestion des Dépendances de Base de Données ---
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """
    Crée et retourne une connexion à la base de données PostgreSQL.
    Cette fonction est une dépendance FastAPI, ce qui la rend remplaçable pour les tests.
    """
    if not DATABASE_URL:
        # Gère le cas où l'URL n'est pas configurée, notamment dans certains tests
        raise HTTPException(status_code=500, detail="La variable d'environnement DATABASE_URL n'est pas configurée.")
    
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

# --- Endpoints de l'API ---

@app.get("/latest-price", summary="Récupérer le dernier prix du Bitcoin")
def get_latest_price(conn = Depends(get_db_connection)):
    """
    Retourne le dernier enregistrement de prix disponible pour le Bitcoin.
    """
    logging.info("Requête reçue pour le dernier prix.")
    try:
        # Utilise DictCursor pour obtenir des résultats sous forme de dictionnaire
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()

        if row:
            logging.info("Dernier prix trouvé et retourné.")
            return dict(row) # Convertit le DictRow en dictionnaire standard
        else:
            logging.warning("Aucune donnée de prix trouvée dans la base.")
            raise HTTPException(status_code=404, detail="Aucune donnée de prix disponible")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du dernier prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/price-history", summary="Récupérer l'historique des prix")
def get_price_history(limit: int = 24, conn = Depends(get_db_connection)):
    """
    Retourne une liste des derniers prix enregistrés, avec une limite configurable.
    """
    logging.info(f"Requête reçue pour l'historique des prix (limite={limit}).")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # PostgreSQL utilise %s comme placeholder pour les paramètres
            cursor.execute("SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT %s", (limit,))
            rows = cursor.fetchall()
        
        logging.info(f"{len(rows)} enregistrements d'historique trouvés.")
        return [dict(row) for row in rows]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'historique des prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/latest-news", summary="Récupérer les dernières actualités")
def get_latest_news(limit: int = 5, conn = Depends(get_db_connection)):
    """
    Retourne une liste des dernières actualités sur le Bitcoin.
    """
    logging.info(f"Requête reçue pour les dernières nouvelles (limite={limit}).")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT title, link, content, timestamp FROM bitcoin_news ORDER BY id DESC LIMIT %s", (limit,))
            rows = cursor.fetchall()
        
        logging.info(f"{len(rows)} actualités trouvées.")
        return [dict(row) for row in rows]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des nouvelles : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/price-analysis", summary="Obtenir une analyse IA de la tendance des prix")
def price_analysis(limit: int = 24, conn = Depends(get_db_connection)):
    """
    Fournit une analyse textuelle de la tendance des prix du Bitcoin générée par une IA.
    """
    logging.info(f"Requête reçue pour l'analyse de prix (limite={limit}).")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT timestamp, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT %s", (limit,))
            rows = cursor.fetchall()

        if not rows:
            logging.warning(f"Pas assez de données pour l'analyse (limite={limit}).")
            raise HTTPException(status_code=404, detail="Pas assez de données pour l'analyse")

        formatted_history = "\n".join(
            [f"Date (timestamp {row['timestamp']}): Prix de clôture = {row['close']}$" for row in rows]
        )
        prompt = (
            "Tu es un analyste financier pour un débutant. "
            "Basé sur l'historique de prix du Bitcoin suivant, quelle est la tendance générale (haussière, baissière, ou stable) ? "
            "Réponds en 2 phrases maximum, en mentionnant si le marché semble volatil ou non.\n\n"
            f"Données:\n{formatted_history}"
        )

        logging.info("Appel au service d'analyse IA (Gemini)...")
        analysis_result = analyze_text(prompt)
        logging.info("Analyse IA reçue avec succès.")

        return {"analysis": analysis_result}

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erreur critique lors de l'analyse de prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur lors de l'analyse IA")