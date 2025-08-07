import os
import requests
import time
from dotenv import load_dotenv
# On importe la nouvelle fonction
from stockage import init_db, insert_many_prices

load_dotenv()

API_KEY = os.getenv("COINALYZE_API")
API_URL = "https://api.coinalyze.net/v1/ohlcv-history"
symbols = "BTCUSDC.A"
interval = "1hour"

TO_TIMESTAMP = int(time.time())
# On récupère 25 heures pour être sûr d'avoir 24 points complets
FROM_TIMESTAMP = TO_TIMESTAMP - (25 * 60 * 60)

HEADERS = {
    "api_key" : API_KEY
}

def get_bitcoin_data():
    params = {
        "symbols": symbols,
        "interval": interval,
        "from": FROM_TIMESTAMP,
        "to": TO_TIMESTAMP
    }
    
    try:
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status() # Lève une erreur pour les statuts 4xx/5xx
        print("Connexion réussie !")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API Coinalyze: {e}")
        return None

if __name__ == "__main__":
    # Pas besoin d'appeler init_db() ici si les services le font déjà,
    # mais c'est une sécurité.
    init_db()
    data = get_bitcoin_data()
    
    if data and data[0].get("history"):
        history = data[0]["history"]
        data_list = [
            {
                "timestamp": entry["t"],
                "open": entry["o"],
                "high": entry["h"],
                "low": entry["l"],
                "close": entry["c"],
                "volume": entry["v"]
            }
            for entry in history
        ]
        # On appelle la nouvelle fonction qui sait parler à PostgreSQL
        insert_many_prices(data_list)
    else:
        print("Aucune donnée de prix reçue de l'API ou format inattendu.")
