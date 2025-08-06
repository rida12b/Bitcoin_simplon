import os
import requests
import time
from dotenv import load_dotenv
# MODIFIÉ : Importe les nouvelles fonctions
from stockage import init_db, insert_many_prices

load_dotenv()

API_KEY = os.getenv("COINALYZE_API")
API_URL = "https://api.coinalyze.net/v1/ohlcv-history"

def get_bitcoin_data():
    print("Lancement de l'extraction des prix depuis l'API...")
    params = {
        "symbols": "BTCUSDC.A",
        "interval": "1hour",
        "from": int(time.time()) - (24 * 60 * 60),
        "to": int(time.time())
    }
    headers = {"api_key": API_KEY}
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        print("Connexion à l'API Coinalyze réussie !")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à l'API Coinalyze : {e}")
        return None

if __name__ == "__main__":
    init_db()
    data = get_bitcoin_data()
    if data and data[0].get("history"):
        history = data[0]["history"]
        data_list = [
            {
                "timestamp": entry["t"], "open": entry["o"], "high": entry["h"],
                "low": entry["l"], "close": entry["c"], "volume": entry["v"]
            } for entry in history
        ]
        # MODIFIÉ : Appelle la fonction spécifique aux prix
        insert_many_prices(data_list)
    else:
        print("🟡 Aucune donnée de prix reçue de l'API.")
