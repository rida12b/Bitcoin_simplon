# Rapport de Projet de Certification

**Titre du Projet :** Bitcoin Analyzer
**Candidat :** Ridab
**Date :** 2024-07-29
**Certification Visée :** RNCP37827 - Développeur en Intelligence Artificielle

---

## Sommaire
1.  [Introduction et Contexte du Projet](#1-introduction-et-contexte-du-projet)
2.  [Architecture Technique et Choix Technologiques](#2-architecture-technique-et-choix-technologiques)
3.  [Mise en Œuvre - Bloc 1 : La Chaîne de la Donnée](#3-mise-en-œuvre---bloc-1--la-chaîne-de-la-donnée)
    -   [C1 : Automatisation de l'Extraction de Données](#c1--automatisation-de-lextraction-de-données)
    -   [C3 : Agrégation et Nettoyage des Données](#c3--agrégation-et-nettoyage-des-données)
    -   [C4 : Création et Gestion de la Base de Données](#c4--création-et-gestion-de-la-base-de-données)
    -   [C5 : Développement d'une API REST de Mise à Disposition](#c5--développement-dune-api-rest-de-mise-à-disposition)
4.  [Mise en Œuvre - Bloc 2 : Intégration d'un Service d'IA](#4-mise-en-œuvre---bloc-2--intégration-dun-service-dia)
    -   [C9 : Exposition d'un Modèle d'IA via une API](#c9--exposition-dun-modèle-dia-via-une-api)
5.  [Mise en Œuvre - Bloc 3 : Tests Automatisés et Qualité du Code](#5-mise-en-œuvre---bloc-3--tests-automatisés-et-qualité-du-code)
    -   [C12 : Tests du Module d'IA et Monitoring](#c12--tests-du-module-dia-et-monitoring)
    -   [C18 : Tests d'API et Validation des Endpoints](#c18--tests-dapi-et-validation-des-endpoints)
    -   [C21 : Refactorisation pour la Testabilité](#c21--refactorisation-pour-la-testabilité)
6.  [Mise en Œuvre - Bloc 4 : MLOps et Intégration Continue](#6-mise-en-œuvre---bloc-4--mlops-et-intégration-continue)
    -   [C13 : Mise en Place de la CI/CD avec GitHub Actions](#c13--mise-en-place-de-la-cicd-avec-github-actions)
    -   [C19 : Automatisation des Tests et Déploiement](#c19--automatisation-des-tests-et-déploiement)
7.  [Gestion de Projet et Incidents](#7-gestion-de-projet-et-incidents)
    -   [Incident CI/CD : ModuleNotFoundError](#incident-cicd--modulenotfounderror)
8.  [Conclusion et Perspectives](#8-conclusion-et-perspectives)

---

## 1. Introduction et Contexte du Projet
*(Compétences C14 : Analyser le besoin, C15 : Concevoir le cadre technique)*

Le projet "Bitcoin Analyzer" vise à répondre à un besoin utilisateur clair : accéder à des informations fiables, centralisées et analysées sur le Bitcoin. Face à la volatilité des cryptomonnaies et à la dispersion des sources d'information, ce projet propose une solution intégrée qui automatise le processus de collecte, de stockage et d'analyse.

L'objectif est de construire un service capable de fournir non seulement des données de marché brutes (prix, volume) et des actualités, mais également une analyse de tendance générée par une intelligence artificielle. Ce service est exposé via une API RESTful, le rendant facilement consommable par de futures applications (tableau de bord web, application mobile, etc.).

## 2. Architecture Technique et Choix Technologiques
*(Compétence C15 : Concevoir le cadre technique)*

L'architecture du projet a été conçue pour être modulaire et évolutive.

-   **Langage et Ecosystème :** **Python** a été choisi pour sa polyvalence, son écosystème riche en bibliothèques pour la science des données (`requests`, `beautifulsoup`) et le développement web (`fastapi`).
-   **Collecte de Données :**
    -   Un script `extraction_api.py` interroge l'API Coinalyze pour les données de marché.
    -   Un script `extraction_news.py` scrape le site `bitcoinmagazine.com` pour les actualités.
-   **Stockage de Données :** **SQLite** a été retenu pour sa simplicité de mise en œuvre et sa légèreté, ce qui est idéal pour un projet de cette envergure. Un module `stockage.py` centralise la gestion de la base pour assurer la cohérence.
-   **API Backend :** **FastAPI** a été choisi pour sa haute performance, sa validation de données basée sur Pydantic, et sa capacité à générer automatiquement une documentation interactive (Swagger UI), ce qui est un atout majeur pour la maintenabilité.
-   **Service d'IA :** **Google Gemini** a été sélectionné comme modèle de langage pour sa performance et sa facilité d'intégration. La logique d'appel est isolée dans un module `llm_analyzer.py`.

## 3. Mise en Œuvre - Bloc 1 : La Chaîne de la Donnée

### C1 : Automatisation de l'Extraction de Données

L'extraction est automatisée via deux scripts Python distincts, chacun ciblant une source de nature différente.

-   **Extraction depuis une API REST (Coinalyze) :** Le script `extraction_api.py` gère la connexion à une API externe. Les informations sensibles comme la clé d'API sont gérées via un fichier `.env` et la bibliothèque `python-dotenv`, garantissant qu'elles ne sont pas exposées dans le code source.

    *Extrait de code commenté de `scripts/extraction_api.py` :*
    ```python
    # Import des bibliothèques nécessaires
    import os
    import requests
    from dotenv import load_dotenv

    # Chargement des variables d'environnement (contient l'API_KEY)
    load_dotenv()
    API_KEY = os.getenv("COINALYZE_API_KEY")

    def get_bitcoin_data():
        # Configuration des paramètres de la requête
        params = {"symbols": "BTCUSDT.A", "interval": "1hour", ...}
        headers = {"api_key": API_KEY}
        
        # Le bloc try/except assure la robustesse en cas d'échec de la connexion
        try:
            response = requests.get(API_URL, headers=headers, params=params)
            # Lève une exception pour les codes d'erreur (4xx ou 5xx)
            response.raise_for_status()  
            print("Connexion à l'API Coinalyze réussie !")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"Erreur HTTP: {http_err}")
            return None
    ```

-   **Extraction depuis une page Web (Scraping) :** Le script `extraction_news.py` utilise `requests` pour télécharger le contenu HTML de la page d'actualités et `BeautifulSoup` pour le parser. Un `User-Agent` est spécifié dans les en-têtes pour simuler un navigateur et éviter les blocages.

### C3 : Agrégation et Nettoyage des Données

Une fois extraites, les données brutes sont nettoyées et formatées avant d'être stockées. Cette étape est essentielle pour garantir la qualité et l'homogénéité du jeu de données final.
-   Pour les prix, les données JSON de l'API sont transformées en une liste de dictionnaires Python avec des clés normalisées (`timestamp`, `open`, `high`, `low`, `close`, `volume`).
-   Pour les actualités, les éléments HTML scrapés sont convertis en une liste de dictionnaires (`title`, `link`, `content`, `timestamp`).

### C4 : Création et Gestion de la Base de Données

Une base de données SQLite unique, `data/bitcoin.db`, est utilisée pour centraliser toutes les données.
-   **Modèle Physique des Données :** Le script `scripts/stockage.py` contient la fonction `init_db()` qui définit le schéma des tables.
    *Extrait SQL de la création des tables dans `init_db()` :*
    ```sql
    -- Table pour stocker les prix du Bitcoin, avec un timestamp unique
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER UNIQUE,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    );

    -- Table pour stocker les actualités, avec un titre unique
    CREATE TABLE IF NOT EXISTS bitcoin_news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        content TEXT,
        timestamp DATETIME
    );
    ```
-   **Intégrité des Données :** L'unicité des données est garantie au niveau de la base grâce aux contraintes `UNIQUE` sur `timestamp` et `title`. Les insertions sont effectuées avec la commande `INSERT OR IGNORE` pour éviter les erreurs de duplication et rendre les scripts d'extraction ré-exécutables sans effet de bord.

### C5 : Développement d'une API REST de Mise à Disposition

L'accès aux données est fourni par une API développée avec FastAPI.
-   **Endpoints :** L'API expose des endpoints clairs et intuitifs pour chaque ressource : `/latest-price`, `/price-history`, `/latest-news`.
-   **Documentation Automatique (Swagger UI) :** L'un des atouts majeurs de FastAPI est la génération automatique d'une documentation interactive. En accédant à l'URL `/docs`, l'utilisateur (ou un autre développeur) peut visualiser tous les endpoints, leurs paramètres, et même les tester directement depuis le navigateur. Ce livrable est crucial pour assurer la maintenabilité et l'interopérabilité de l'API.

## 4. Mise en Œuvre - Bloc 2 : Intégration d'un Service d'IA

### C9 : Exposition d'un Modèle d'IA via une API

La compétence clé ici est de ne pas seulement servir des données, mais d'exposer une fonctionnalité intelligente. Le endpoint `/price-analysis` a été créé à cet effet.
-   **Processus d'Analyse :**
    1.  L'API récupère l'historique des prix depuis la base de données.
    2.  Elle formate ces données en un **prompt** spécifiquement conçu pour guider le modèle de langage.
    3.  Elle appelle la fonction `analyze_text()` qui contient la logique d'appel à l'API de Google Gemini.
    4.  Elle retourne la réponse textuelle du modèle, encapsulée dans un JSON.
-   **Prompt Engineering :** Le prompt est soigneusement rédigé pour définir le rôle du modèle ("Tu es un analyste financier pour un débutant"), le contexte, la question précise, et le format de réponse attendu.

    *Extrait de code commenté de `api/app.py` :*
    ```python
    @app.get("/price-analysis")
    def price_analysis(limit: int = 24):
        try:
            # Étape 1: Récupération des données depuis la BDD
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, close FROM bitcoin_prices ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                return {"error": "Pas assez de données pour l'analyse."}

            # Étape 2: Formatage des données et création du prompt
            formatted_history = "\n".join([f"Timestamp {row[0]}: Clôture à {row[1]}$" for row in rows])
            prompt = (
                "Tu es un analyste financier pour un débutant. "
                "Basé sur l'historique de prix suivant, quelle est la tendance générale (haussière, baissière, ou stable) ? "
                "Réponds en 2 phrases maximum.\n\n"
                f"Données:\n{formatted_history}"
            )

            # Étape 3: Appel du service d'analyse IA
            analysis_result = analyze_text(prompt)

            # Étape 4: Retour du résultat
            return {"analysis": analysis_result}

        except Exception as e:
            # Gestion des erreurs (ex: clé API du LLM non configurée)
            return {"error": str(e)}
    ```

## 5. Mise en Œuvre - Bloc 3 : Tests Automatisés et Qualité du Code

### C12 : Tests du Module d'IA et Monitoring

La mise en place de tests pour le module d'IA représente un défi particulier en raison de la nature externe et potentiellement coûteuse des appels API. La solution mise en œuvre illustre les bonnes pratiques du MLOps.

#### Stratégie de Test avec Mocking

La fonction `analyze_text()` du module `llm_analyzer.py` fait appel à l'API Google Gemini. Pour tester cette fonction sans générer de coûts et garantir la reproductibilité, la technique du **mocking** a été utilisée.

*Extrait de code de `tests/test_llm_analyzer.py` :*
```python
import unittest
from unittest.mock import patch, MagicMock
from scripts.llm_analyzer import analyze_text

class TestLLMAnalyzer(unittest.TestCase):
    
    @patch('scripts.llm_analyzer.model.generate_content')
    def test_analyze_text_success(self, mock_generate):
        # Configuration du mock pour simuler une réponse réussie
        mock_response = MagicMock()
        mock_response.text = "Analyse générée par l'IA"
        mock_generate.return_value = mock_response
        
        # Test de la fonction
        result = analyze_text("Test prompt")
        
        # Vérifications
        self.assertEqual(result, "Analyse générée par l'IA")
        mock_generate.assert_called_once_with("Test prompt")
```

#### Avantages de cette Approche

1. **Rapidité** : Les tests s'exécutent en millisecondes au lieu d'attendre la réponse de l'API
2. **Coût** : Aucun coût d'API engagé lors des tests
3. **Fiabilité** : Tests indépendants de la connexion internet et de la disponibilité du service
4. **Contrôle** : Possibilité de tester différents scénarios (succès, échec, timeout)

Cette approche permet de valider la logique métier (création des prompts, traitement des réponses) sans dépendre de services externes, une compétence essentielle en MLOps.

### C18 : Tests d'API et Validation des Endpoints

Le développement de tests pour l'API FastAPI a nécessité la mise en place d'une infrastructure de test dédiée pour garantir l'isolation et la reproductibilité.

#### Infrastructure de Test

Un défi majeur était que les tests s'exécutaient dans un environnement isolé, sans accès à la base de données principale. La solution adoptée illustre les bonnes pratiques de développement :

*Extrait de `tests/setup_test_db.py` :*
```python
import sqlite3
import os
from scripts.stockage import init_db, insert_many

def setup_test_database():
    """Crée une base de données de test avec des données prévisibles"""
    test_db_path = "tests/test_database.db"
    
    # Suppression de l'ancienne base si elle existe
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Création de la nouvelle base avec schéma
    init_db(test_db_path)
    
    # Insertion de données de test prévisibles
    test_news = [{"title": "Test Bitcoin News", "link": "http://test.com", 
                 "content": "Test content", "timestamp": "2024-01-01 12:00:00"}]
    test_prices = [
        {"timestamp": 1704067200, "open": 45000, "high": 46000, "low": 44000, "close": 45500, "volume": 1000},
        {"timestamp": 1704070800, "open": 45500, "high": 46500, "low": 45000, "close": 46000, "volume": 1200},
        {"timestamp": 1704074400, "open": 46000, "high": 47000, "low": 45500, "close": 46500, "volume": 1100}
    ]
    
    insert_many(test_news, "bitcoin_news", test_db_path)
    insert_many(test_prices, "bitcoin_prices", test_db_path)
```

#### Tests des Endpoints

Le fichier `tests/test_api.py` utilise le `TestClient` de FastAPI pour simuler des requêtes HTTP et valider les réponses :

*Extrait de `tests/test_api.py` :*
```python
from fastapi.testclient import TestClient
from api.app import app

# Configuration pour utiliser la base de données de test
app.dependency_overrides[get_database] = lambda: "tests/test_database.db"

client = TestClient(app)

def test_latest_news():
    """Test de l'endpoint /latest-news"""
    response = client.get("/latest-news")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Bitcoin News"

def test_price_history():
    """Test de l'endpoint /price-history"""
    response = client.get("/price-history?limit=2")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["close"] == 46500  # Prix le plus récent
```

### C21 : Refactorisation pour la Testabilité

Au cours de la mise en place des tests, une limitation importante du code existant a été identifiée : le module `stockage.py` était difficile à tester en raison de dépendances globales codées en dur.

#### Problème Initial

Les fonctions du module `stockage.py` utilisaient un chemin de base de données codé en dur :
```python
DB_PATH = "data/bitcoin.db"  # Chemin global

def init_db():
    conn = sqlite3.connect(DB_PATH)  # Dépendance codée en dur
    # ... logique de création
```

#### Solution : Injection de Dépendances

Le code a été refactorisé pour appliquer le principe d'Inversion de Dépendance :
```python
def init_db(db_path="data/bitcoin.db"):
    """Initialise la base de données avec un chemin configurable"""
    conn = sqlite3.connect(db_path)
    # ... logique de création

def insert_many(data, table_name, db_path="data/bitcoin.db"):
    """Insère des données avec un chemin de base configurable"""
    conn = sqlite3.connect(db_path)
    # ... logique d'insertion
```

#### Bénéfices de cette Refactorisation

1. **Testabilité** : Les tests peuvent utiliser leur propre base de données
2. **Flexibilité** : Le code peut facilement être adapté pour différents environnements
3. **Isolation** : Les tests n'interfèrent pas avec la base de données principale
4. **Maintenabilité** : Le code respecte les principes SOLID

Cette refactorisation illustre comment l'écriture de tests peut améliorer la qualité du code en exposant les défauts de conception.

## 6. Mise en Œuvre - Bloc 4 : MLOps et Intégration Continue

### C13 : Mise en Place de la CI/CD avec GitHub Actions

L'intégration continue est essentielle pour maintenir la qualité du code et garantir la reproductibilité des environnements, particulièrement critique dans les projets d'IA où les dépendances peuvent être complexes.

#### Configuration du Workflow

Le fichier `.github/workflows/ci.yml` définit un pipeline automatisé qui se déclenche à chaque modification du code :

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Set up test database
      run: |
        python tests/setup_test_db.py
    
    - name: Run tests
      run: |
        pytest tests/ -v
```

#### Avantages de cette Configuration

1. **Automatisation** : Chaque commit déclenche automatiquement les tests
2. **Environnement Propre** : Chaque build part d'un environnement Ubuntu vierge
3. **Reproductibilité** : Les dépendances sont installées à partir de `requirements.txt`
4. **Validation** : Le code ne peut être mergé que si les tests passent

### C19 : Automatisation des Tests et Déploiement

La CI/CD permet d'automatiser l'exécution de l'ensemble de la suite de tests, combinant les tests unitaires (module IA) et les tests d'intégration (API).

#### Pipeline de Validation

Le pipeline suit une séquence logique :

1. **Préparation de l'environnement** : Installation de Python et des dépendances
2. **Configuration des données** : Création de la base de données de test
3. **Exécution des tests** : Lancement de pytest avec reporting détaillé
4. **Validation** : Succès ou échec du build basé sur les résultats des tests

#### Métriques et Monitoring

Le système peut être étendu pour inclure des métriques de qualité :
- Couverture de code
- Temps d'exécution des tests
- Détection de régressions de performance

Cette approche garantit que chaque modification du code est validée dans un environnement standardisé, réduisant les risques de déploiement.

## 7. Gestion de Projet et Incidents

### Incident CI/CD : ModuleNotFoundError

Un incident significatif s'est produit lors de la mise en place de la CI/CD, illustrant parfaitement l'utilité de cette approche pour détecter les problèmes de reproductibilité.

#### Description de l'Incident

- **Date** : Décembre 2024
- **Symptôme** : Échec du premier workflow GitHub Actions
- **Erreur** : `ModuleNotFoundError: No module named 'httpx'`
- **Contexte** : Le code fonctionnait parfaitement en local

#### Diagnostic et Résolution

1. **Investigation** : L'erreur indiquait que le module `httpx` était manquant dans l'environnement CI
2. **Cause Racine** : La dépendance `httpx` avait été installée manuellement en local mais n'était pas présente dans `requirements.txt`
3. **Solution** : Ajout de `httpx` dans le fichier `requirements.txt`
4. **Validation** : Nouveau commit, workflow passé au vert

#### Leçons Apprises

Cet incident démontre plusieurs points cruciaux :

1. **Valeur de la CI** : Sans la CI, ce problème n'aurait été découvert qu'au déploiement
2. **Importance de `requirements.txt`** : Toutes les dépendances doivent être explicitement déclarées
3. **Reproductibilité** : L'environnement de développement doit être identique à l'environnement de production
4. **Détection Précoce** : Les problèmes sont détectés immédiatement, pas lors du déploiement

### Résolution d'Incident Technique Antérieur (C21)

Un incident technique critique antérieur avait également été résolu :

-   **Date de l'incident :** 29/07/2024
-   **Symptôme :** L'API retournait une erreur 500 sur les endpoints liés aux prix (`/price-history`, `/price-analysis`), alors que l'endpoint des actualités (`/latest-news`) fonctionnait.
-   **Diagnostic :** L'ajout d'une capture d'exception dans le code de l'API a permis d'isoler le message d'erreur précis : `sqlite3.OperationalError: no such table: bitcoin_prices`.
-   **Cause Racine :** Une investigation des scripts a révélé que deux fichiers de base de données étaient créés par erreur. Le module `stockage.py` (utilisé par le script des prix) créait une base `bitcoin_data.db` à la racine, tandis que le reste de l'application utilisait `data/bitcoin.db`. L'API cherchait donc la table des prix dans un fichier qui ne la contenait pas.
-   **Résolution :**
    1.  Le chemin de la base de données a été centralisé et corrigé dans `scripts/stockage.py` pour pointer exclusivement vers `data/bitcoin.db`.
    2.  Le fichier de base de données erroné a été supprimé.
    3.  Les scripts de collecte ont été ré-exécutés pour peupler la base de données unique et correcte.
-   **Validation :** Après redémarrage du serveur, tous les endpoints fonctionnaient comme attendu.
-   **Leçons Apprises :** Cet incident a souligné l'importance de la centralisation de la configuration, de la journalisation des erreurs précises, et de la mise en place de tests d'intégration de base.

## 8. Conclusion et Perspectives

Ce projet a permis de construire une chaîne de traitement de la donnée complète et fonctionnelle, de la collecte automatisée à l'exposition d'une analyse par IA via une API REST, avec une approche professionnelle incluant tests automatisés et intégration continue.

### Compétences Validées

Le projet couvre exhaustivement les compétences du référentiel RNCP37827 :

**Bloc 1 - La Chaîne de la Donnée :**
- **C1** : Automatisation de l'extraction via API et scraping
- **C3** : Agrégation et nettoyage des données
- **C4** : Conception et gestion de base de données SQLite
- **C5** : Développement d'API REST avec FastAPI

**Bloc 2 - Intégration d'IA :**
- **C9** : Exposition de modèle d'IA (Google Gemini) via API

**Bloc 3 - Tests et Qualité :**
- **C12** : Tests unitaires du module IA avec stratégies de mocking
- **C18** : Tests d'API avec infrastructure de test dédiée
- **C21** : Refactorisation pour la testabilité (injection de dépendances)

**Bloc 4 - MLOps et DevOps :**
- **C13** : Mise en place CI/CD avec GitHub Actions
- **C19** : Automatisation des tests et validation continue

### Approche Méthodologique

Le projet illustre plusieurs bonnes pratiques professionnelles :

1. **Tests Automatisés** : Stratégies de mocking pour l'IA, infrastructure de test isolée
2. **Intégration Continue** : Pipeline automatisé validant chaque modification
3. **Reproductibilité** : Environnements standardisés via `requirements.txt`
4. **Gestion d'Incidents** : Documentation et résolution méthodique des problèmes
5. **Refactorisation** : Amélioration continue de la qualité du code

### Valeur Ajoutée du MLOps

L'intégration des pratiques MLOps apporte une valeur significative :

- **Fiabilité** : Détection précoce des problèmes via la CI
- **Maintenabilité** : Code testable et modulaire
- **Collaboration** : Validation automatique des contributions
- **Qualité** : Tests garantissant le bon fonctionnement

### Perspectives d'Amélioration

Les prochaines étapes pour faire évoluer le projet incluent :

1. **Infrastructure** : Déploiement sur infrastructure cloud (AWS, Azure)
2. **Base de Données** : Migration vers PostgreSQL pour la scalabilité
3. **Interface Utilisateur** : Développement d'une interface web (Django frontend)
4. **Monitoring Avancé** : Métriques de performance et alertes
5. **Sécurité** : Authentification et autorisation
6. **Scalabilité** : Containerisation avec Docker et orchestration

### Impact Professionnel

Ce projet démontre une maîtrise complète des compétences attendues d'un Développeur en Intelligence Artificielle, combinant :
- Expertise technique (collecte, traitement, exposition de données)
- Compétences en IA (intégration de modèles de langage)
- Pratiques DevOps (tests, CI/CD, reproductibilité)
- Approche méthodologique (documentation, gestion d'incidents)

L'approche adoptée respecte les standards de l'industrie et prépare efficacement aux défis professionnels du développement d'applications d'IA en production. 