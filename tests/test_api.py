# tests/test_api.py
import sys
import os
import sqlite3
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.app import app, get_db_connection

# --- NOUVELLE LOGIQUE ---
# Cette fonction de substitution va maintenant lire la même variable d'environnement
# que notre script setup_test_db.py a configurée.
def override_get_db_connection():
    # On récupère le chemin de la BDD depuis la variable d'environnement
    # La variable commence par "sqlite:///", on doit enlever ce préfixe.
    db_path_str = os.environ.get("DATABASE_URL")
    if db_path_str and db_path_str.startswith("sqlite:///"):
        db_path = db_path_str[10:] # Enlève "sqlite:///"
        conn = sqlite3.connect(db_path)
        try:
            yield conn
        finally:
            conn.close()
    else:
        raise Exception("DATABASE_URL pour les tests n'est pas configurée correctement en mode SQLite.")

# On applique la surcharge
app.dependency_overrides[get_db_connection] = override_get_db_connection

# Le reste du fichier ne change pas
client = TestClient(app)

def test_get_latest_news():
    """Teste si l'API retourne bien la nouvelle de test depuis la BDD SQLite."""
    response = client.get("/latest-news")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]['title'] == "Titre de test"

def test_get_price_history():
    """Teste si l'API retourne bien l'historique de prix de test depuis la BDD SQLite."""
    response = client.get("/price-history?limit=3")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_root_path_health_check():
    """
    Teste un endpoint simple pour vérifier que l'API est en vie.
    """
    response = client.get("/latest-news") # On utilise un endpoint qui existe
    assert response.status_code == 200
