from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from stockage import init_db
import sqlite3
from llm_analyzer import analyze_text
from fastapi import Body

app = FastAPI()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/bitcoin.db")
@app.get("/latest-price")
def get_latest_price():
    conn = sqlite3.connect("bitcoin_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "timestamp": row[0],
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5]
        }
    else:
        return {"error": "Aucune donnée disponible"}
    
@app.get("/price-history")
def get_price_history(limit: int = 24):
    conn = sqlite3.connect("bitcoin_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, open, high, low, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "timestamp": row[0],
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5]
        }
        for row in rows
    ]





@app.get("/latest-news")
def get_latest_news(limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, link, content, timestamp FROM bitcoin_news ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "title": row[0],
            "link": row[1],
            "content": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]



@app.get("/price-analysis")
def price_analysis(limit: int = 24):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, close, volume FROM bitcoin_prices ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"error": "Pas assez de données pour l'analyse."}

        # Formater les données pour le prompt de l'IA
        # rows est une liste de tuples (timestamp, close, volume)
        formatted_history = "\n".join(
            [f"Date (timestamp {row[0]}): Prix de clôture = {row[1]}$" for row in rows]
        )
        prompt = (
            "Tu es un analyste financier pour un débutant. "
            "Basé sur l'historique de prix du Bitcoin suivant, quelle est la tendance générale (haussière, baissière, ou stable) ? "
            "Réponds en 2 phrases maximum, en mentionnant si le marché semble volatil ou non.\n\n"
            f"Données:\n{formatted_history}"
        )

        # Appeler le service d'analyse IA
        analysis_result = analyze_text(prompt)

        return {"analysis": analysis_result}

    except Exception as e:
        return {"error": str(e)}