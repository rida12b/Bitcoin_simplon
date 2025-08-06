import sys
import os
import sqlite3
from fastapi.testclient import TestClient

# --- Imports ---
# Permet de trouver les modules 'api' et 'scripts'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# On importe l'application FastAPI ET la nouvelle fonction de dépendance
from api.app import app, get_db_connection

# --- Configuration de la Base de Données de TEST ---

# Chemin de notre base de données de test SQLite
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')

# C'est notre fausse fonction de connexion. Elle sera utilisée UNIQUEMENT pendant les tests.
# Elle se connecte à notre fichier SQLite de test.
def override_get_db_connection():
    conn = sqlite3.connect(TEST_DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

# === La Ligne Magique ===
# On dit à FastAPI : "Quand un endpoint demande la dépendance 'get_db_connection',
# ne lui donne pas la vraie (PostgreSQL), mais donne-lui plutôt ma fausse fonction 'override_get_db_connection' (SQLite)".
app.dependency_overrides[get_db_connection] = override_get_db_connection


# --- Client de Test ---
# Le client est créé APRÈS avoir défini le "override".
# Il utilisera donc la base de données SQLite pour tous ses appels.
client = TestClient(app)


# --- Tests ---
# Ces fonctions de test n'ont pas besoin de changer !
# Elles appellent l'API, et grâce au "override", l'API répondra en utilisant les données de la BDD de test SQLite.

def test_get_latest_news():
    """Teste si l'API retourne bien la nouvelle de test depuis la BDD SQLite."""
    response = client.get("/latest-news")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Assurez-vous que votre setup_test_db.py insère bien au moins une nouvelle de test
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
    On utilise /latest-news car il est censé toujours répondre.
    """
    response = client.get("/latest-news")
    assert response.status_code == 200