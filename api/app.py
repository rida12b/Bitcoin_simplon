from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from stockage import init_db
import sqlite3
app = FastAPI()

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