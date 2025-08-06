import os
import requests
import time
from dotenv import load_dotenv
import psycopg2

load_dotenv()

API_KEY = os.getenv("COINALYZE_API")
API_URL = "https://api.coinalyze.net/v1/ohlcv-history"
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_bitcoin_data():
    # ... (le reste de la fonction ne change pas)
    params = { "symbols": "BTCUSDC.A", "interval": "1hour", "from": int(time.time()) - (24 * 60 * 60), "to": int(time.time()) }
    headers = {"api_key" : API_KEY}
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        print("Connexion API réussie !")
        return response.json()
    else:
        print(f"Erreur API {response.status_code} : {response.text}")
        return None

if __name__ == "__main__":
    if not DATABASE_URL:
        print("Erreur: DATABASE_URL n'est pas configurée.")
    else:
        data = get_bitcoin_data()
        if data and data[0]["history"]:
            history = data[0]["history"]
            to_insert = [
                (entry["t"], entry["o"], entry["h"], entry["l"], entry["c"], entry["v"])
                for entry in history
            ]
            try:
                with psycopg2.connect(DATABASE_URL) as conn:
                    with conn.cursor() as cursor:
                        # INSERT ... ON CONFLICT (timestamp) DO NOTHING; gère les doublons
                        psycopg2.extras.execute_values(
                            cursor,
                            "INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume) VALUES %s ON CONFLICT (timestamp) DO NOTHING",
                            to_insert
                        )
                print(f"{len(to_insert)} lignes de prix traitées.")
            except Exception as e:
                print(f"Erreur de base de données (API): {e}")
        else:
            print("Aucune donnée de prix à insérer.")