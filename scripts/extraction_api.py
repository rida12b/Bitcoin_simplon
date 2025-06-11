import os
import requests
import time
from dotenv import load_dotenv
from stockage import init_db, insert_many

load_dotenv()

API_KEY = os.getenv("COINALYZE_API")
API_URL = "https://api.coinalyze.net/v1/ohlcv-history"
symbols = "BTCUSDC.A"
interval = "1hour"

TO_TIMESTAMP = int(time.time())
FROM_TIMESTAMP = TO_TIMESTAMP - (24 * 60 * 60)

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
        
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            print("Connexion réussie !")
            data = response.json()
            print(data)
            return data
        else:
            print(f"Erreur {response.status_code} : {response.text}")
            return None

if __name__ == "__main__":
    init_db()
    data = get_bitcoin_data()
    if data:
        # On suppose qu'il n'y a qu'un seul symbole, donc data[0]
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
        insert_many(data_list)
        print(f"{len(data_list)} lignes insérées dans la base.")
    else:
        print("Aucune donnée à insérer.")