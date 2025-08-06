import logging
import sqlite3
import os
import sys
from fastapi import FastAPI, HTTPException
import psycopg2 

# Récupère l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- Configuration du Path (acceptable pour ce projet, mais à revoir pour un projet plus grand) ---
# Ajoute le dossier parent au path pour trouver le module 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.llm_analyzer import analyze_text

# --- Configuration de la Journalisation ---
# Configure le logging pour l'ensemble de l'application API.
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

# --- Configuration de la Base de Données ---
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "bitcoin.db")

# --- Endpoints de l'API ---

@app.get("/latest-price", summary="Récupérer le dernier prix du Bitcoin")
def get_latest_price():
    """
    Retourne le dernier enregistrement de prix disponible pour le Bitcoin.
    """
    logging.info("Requête reçue pour le dernier prix.")
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()

        if row:
            logging.info("Dernier prix trouvé et retourné.")
            return {
                "timestamp": row[0], "open": row[1], "high": row[2],
                "low": row[3], "close": row[4], "volume": row[5]
            }
        else:
            logging.warning("Aucune donnée de prix trouvée dans la base.")
            raise HTTPException(status_code=404, detail="Aucune donnée de prix disponible")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du dernier prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/price-history", summary="Récupérer l'historique des prix")
def get_price_history(limit: int = 24):
    """
    Retourne une liste des derniers prix enregistrés, avec une limite configurable.
    """
    logging.info(f"Requête reçue pour l'historique des prix (limite={limit}).")
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
        
        logging.info(f"{len(rows)} enregistrements d'historique trouvés.")
        return [
            {
                "timestamp": row[0], "open": row[1], "high": row[2],
                "low": row[3], "close": row[4], "volume": row[5]
            }
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'historique des prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/latest-news", summary="Récupérer les dernières actualités")
def get_latest_news(limit: int = 5):
    """
    Retourne une liste des dernières actualités sur le Bitcoin.
    """
    logging.info(f"Requête reçue pour les dernières nouvelles (limite={limit}).")
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, link, content, timestamp FROM bitcoin_news ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
        
        logging.info(f"{len(rows)} actualités trouvées.")
        return [
            {
                "title": row[0], "link": row[1],
                "content": row[2], "timestamp": row[3]
            }
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des nouvelles : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/price-analysis", summary="Obtenir une analyse IA de la tendance des prix")
def price_analysis(limit: int = 24):
    """
    Fournit une analyse textuelle de la tendance des prix du Bitcoin générée par une IA,
    basée sur les dernières données historiques.
    """
    logging.info(f"Requête reçue pour l'analyse de prix (limite={limit}).")
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()

        if not rows:
            logging.warning(f"Pas assez de données pour l'analyse (limite={limit}).")
            raise HTTPException(status_code=404, detail="Pas assez de données pour l'analyse")

        formatted_history = "\n".join(
            [f"Date (timestamp {row[0]}): Prix de clôture = {row[1]}$" for row in rows]
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
        # Re-lève l'exception HTTP pour qu'elle soit gérée par FastAPI
        raise
    except Exception as e:
        logging.error(f"Erreur critique lors de l'analyse de prix : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur lors de l'analyse IA")