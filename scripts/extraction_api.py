import os
import requests
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras  # Import corrigé et unique

# Charger les variables d'environnement
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("COINALYZE_API")
API_URL = "https://api.coinalyze.net/v1/ohlcv-history"
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_bitcoin_data():
    """Interroge l'API Coinalyze pour récupérer les données OHLCV."""
    params = {
        "symbols": "BTCUSDC.A",
        "interval": "1hour",
        "from": int(time.time()) - (24 * 60 * 60),
        "to": int(time.time())
    }
    headers = {"api_key": API_KEY}
    
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur (4xx/5xx)
        print("Connexion API réussie !")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API : {e}")
        return None

if __name__ == "__main__":
    if not DATABASE_URL:
        print("❌ Erreur: La variable d'environnement DATABASE_URL n'est pas configurée.")
    else:
        data = get_bitcoin_data()
        
        # Vérification robuste que les données existent et ont le bon format
        if data and isinstance(data, list) and data and "history" in data[0] and data[0]["history"]:
            history = data[0]["history"]
            
            # Prépare les données pour une insertion en masse
            to_insert = [
                (entry["t"], entry["o"], entry["h"], entry["l"], entry["c"], entry["v"])
                for entry in history
            ]
            
            try:
                with psycopg2.connect(DATABASE_URL) as conn:
                    with conn.cursor() as cursor:
                        # Utilise execute_values pour une insertion efficace
                        # ON CONFLICT gère les doublons de manière robuste
                        extras.execute_values(
                            cursor,
                            "INSERT INTO bitcoin_prices (timestamp, open, high, low, close, volume) VALUES %s ON CONFLICT (timestamp) DO NOTHING",
                            to_insert
                        )
                print(f"💾 {cursor.rowcount} nouvelles lignes de prix insérées.")
            except Exception as e:
                print(f"❌ Erreur de base de données (API): {e}")
        else:
            print("⚠️ Aucune donnée de prix valide à insérer.")