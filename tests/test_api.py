import sys
import os
from fastapi.testclient import TestClient

# --- Imports ---
# Permet de trouver les modules 'api' et 'scripts'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.app import app

# --- Forcer l'API à utiliser la BDD de test ---
# C'est la ligne la plus importante. On modifie directement le chemin
# que l'API utilisera AVANT de créer le TestClient.
import api.app
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')
api.app.DB_PATH = TEST_DB_PATH

# --- Client de Test ---
# Le client est créé APRÈS avoir modifié le chemin de la BDD.
client = TestClient(app)


# --- Tests ---
def test_get_latest_news():
    """Teste si l'API retourne bien la nouvelle de test."""
    response = client.get("/latest-news")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == "Titre de test"

def test_get_price_history():
    """Teste si l'API retourne bien l'historique de prix de test."""
    response = client.get("/price-history?limit=3")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_root_path_health_check():
    """Juste un test pour vérifier que l'API est en vie."""
    # Note : Le endpoint "/" n'existe pas, mais on pourrait en créer un "/health"
    # Pour l'instant, on va tester un endpoint qui existe déjà, comme /latest-news
    response = client.get("/latest-news")
    assert response.status_code == 200