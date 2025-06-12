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
5.  [Mise en Œuvre - Bloc 3 : Gestion de Projet et Incidents](#5-mise-en-œuvre---bloc-3--gestion-de-projet-et-incidents)
    -   [C21 : Résolution et Documentation d'un Incident Technique](#c21--résolution-et-documentation-dun-incident-technique)
6.  [Conclusion et Perspectives](#6-conclusion-et-perspectives)

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

## 5. Mise en Œuvre - Bloc 3 : Gestion de Projet et Incidents

### C21 : Résolution et Documentation d'un Incident Technique

Au cours du développement, un incident technique critique a été rencontré, diagnostiqué et résolu.

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

## 6. Conclusion et Perspectives

Ce projet a permis de construire une chaîne de traitement de la donnée complète et fonctionnelle, de la collecte automatisée à l'exposition d'une analyse par IA via une API REST. Les compétences des blocs 1, 2 et 3 du référentiel ont été mises en pratique, notamment à travers la gestion d'un incident technique réel.

Les perspectives d'amélioration incluent le déploiement de l'application sur une infrastructure cloud, le passage à une base de données plus robuste comme PostgreSQL, et le développement d'une interface web (frontend) pour consommer l'API et présenter les résultats aux utilisateurs finaux. 