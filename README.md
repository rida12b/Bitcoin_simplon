# Bitcoin Analyzer 📈

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![CI](https://github.com/VOTRE_PSEUDO/VOTRE_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/VOTRE_PSEUDO/VOTRE_REPO/actions/workflows/ci.yml)

Bitcoin Analyzer est une application web full-stack, pilotée par l'ia et prête pour la production, conçue pour fournir un tableau de bord complet aux investisseurs en Bitcoin. Elle centralise les données de marché, agrège les actualités pertinentes de manière robuste et offre une analyse de tendance générée par l'ia pour simplifier la prise de décision.

Ce projet a été développé en tant que projet de certification finale pour le titre RNCP Niveau 6 "Développeur en Intelligence Artificielle". Il démontre un ensemble complet de compétences, de l'ingénierie des données à l'intégration de services d'ia, en passant par le développement web full-stack et les pratiques MLOps/DevOps professionnelles.

## 🏛️ Architecture de Production

Le projet est construit sur une architecture cloud distribuée, moderne et découplée pour garantir la scalabilité, la haute disponibilité, la maintenabilité et une séparation claire des responsabilités.

```mermaid
graph TD;
    subgraph "Utilisateur Final"
        U[👤 Investisseur]
    end

    subgraph "Cloud: DigitalOcean (VPS)"
        direction LR
        U -- "Requête HTTPS" --> NGINX[Reverse Proxy Nginx];
        
        subgraph "Services Applicatifs (Gunicorn + Systemd)"
            NGINX -- "Port 8000" --> DJ[Frontend Django];
            NGINX -- "Port 8001" --> FA[Backend API FastAPI];
        end

        DJ -- "Appel API interne" --> FA;
        
        subgraph "Automatisation (Cron)"
            CRON(⏰ Tâche Cron) -- "Exécute `run_scripts.sh` toutes les heures" --> SCRIPTS[Scripts de Collecte];
        end
    end

    subgraph "Cloud: Render (Base de données managée)"
        DB[(🐘 PostgreSQL)];
    end

    subgraph "Services Externes"
        GEMINI[API Google Gemini];
        RSS[Flux RSS Google News];
        COINALYZE[API Coinalyze];
    end

    FA -- "Connexion BDD" --> DB;
    FA -- "Analyse IA" --> GEMINI;
    
    SCRIPTS -- "Écrit les données" --> DB;
    SCRIPTS -- "Lit les données" --> RSS;
    SCRIPTS -- "Lit les données" --> COINALYZE;
```

### Flux de données :

1.  **Collecte Automatisée (toutes les heures)**: Le service Cron sur le VPS exécute les scripts Python qui collectent les données de marché (Coinalyze) et les actualités (Flux RSS), puis les insèrent dans la base de données PostgreSQL hébergée sur Render.
2.  **Requête Utilisateur**: L'utilisateur accède au site via son navigateur. Le reverse proxy Nginx dirige la requête vers l'application Django (port 8000).
3.  **Appel Interne**: La vue Django agit comme un client, appelant l'api FastAPI (port 8001) pour récupérer les données.
4.  **Logique Backend**: L'api FastAPI interroge la base PostgreSQL pour les données stockées et appelle l'api Google Gemini pour générer une analyse de tendance en temps réel.
5.  **Réponse et Affichage**: FastAPI retourne les données à Django, qui les intègre dans un template HTML et renvoie la page web complète à l'utilisateur.

## ✨ Fonctionnalités Clés

### ⚙️ Pipeline d'ingénierie des Données Robuste
- **Collecte Automatisée (Cron)**: Les données sont mises à jour de manière autonome toutes les heures, garantissant la fraîcheur de l'information.
- **Extraction Multi-Source**: Collecte via API REST (Coinalyze) et pivot stratégique vers des Flux RSS (feedparser) pour une fiabilité maximale des actualités, suite à un incident de scraping.
- **Persistance Professionnelle**: Stockage des données dans une base de données PostgreSQL managée, prête pour la production.

### 🚀 API Backend Haute Performance
- Développée avec **FastAPI** et servie par **Gunicorn** pour une réactivité et une robustesse maximales.
- Expose des endpoints clairs pour les prix, l'historique et les actualités.
- Documentation interactive auto-générée avec Swagger UI.

### 🧠 Analyse par IA
- Intégration du modèle **Google Gemini Pro**, choisi après un benchmark formel et objectif.
- Génère des résumés en langage naturel, accessibles aux non-experts.

### 🖥️ Tableau de Bord Frontend Moderne
- Application **Django** servie par **Gunicorn**, agissant comme un client de l'api.
- Interface utilisateur propre et responsive.
- Gestion robuste des erreurs si le service backend est indisponible.

### ✅ Bonnes Pratiques MLOps & DevOps
- **Tests Automatisés**: Suite de tests complète avec `pytest`, incluant des tests unitaires (avec mocking pour l'ia) et des tests d'intégration utilisant une BDD SQLite isolée.
- **Déploiement Continu (CI/CD)**: Pipeline avec **GitHub Actions** qui automatise les tests, le build de l'image Docker, et le déploiement sur le VPS via un script shell (`deploy.sh`).
- **Conteneurisation**: L'api est packagée dans une image **Docker** optimisée.
- **Gestion des Services (Systemd)**: Les applications sont gérées comme des services Linux persistants, garantissant leur redémarrage automatique et leur haute disponibilité.

## 🛠️ Pile Technologique

| Catégorie | Technologie | Rôle |
| :--- | :--- | :--- |
| **Langage** | Python 3.11 | Langage principal du projet. |
| **API Backend** | FastAPI, Gunicorn | Création de l'api REST et serveur d'application de production. |
| **Frontend** | Django, Gunicorn | Framework web pour l'interface utilisateur et serveur de production. |
| **Base de Données** | PostgreSQL (Prod), SQLite (Dev/Test) | Stockage des données de marché et d'actualités. |
| **Service IA** | Google Gemini Pro | Génération des analyses de tendance. |
| **Collecte de Données**| Requests, Feedparser | Communication avec les API externes et les flux RSS. |
| **Tests** | Pytest, Pytest-Mock, Httpx | Framework de test, simulation d'objets, client HTTP pour les tests. |
| **CI/CD & DevOps** | GitHub Actions, Docker, Systemd, Cron | Intégration continue, packaging, gestion des services, planification des tâches. |

## 🚀 Démarrage Rapide (Environnement de Développement Local)

### 1. Prérequis
- Python 3.11 ou supérieur
- Git

### 2. Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/VOTRE_PSEUDO/Bitcoin_simplon.git
    cd Bitcoin_simplon
    ```

2.  **Créez et activez un environnement virtuel :**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurez les variables d'environnement :**
    Créez un fichier `.env` à la racine en vous basant sur le fichier `.env.example`.
    ```env
    # URL de connexion à votre base de données PostgreSQL (pour la prod)
    # Pour le développement local, vous pouvez laisser cette ligne commentée.
    # DATABASE_URL="postgresql://user:password@host/database"

    # Clé API pour le service de données de marché (Coinalyze)
    COINALYZE_API="VOTRE_CLE_API_COINALYZE"

    # Clé API pour le service d'ia (Google Gemini)
    GEMINI_API_KEY="VOTRE_CLE_API_GEMINI"
    ```

5.  **Initialisez la base de données locale (SQLite) :**
    ```bash
    python scripts/setup_source_db.py
    ```

### 3. Lancement de l'application Locale

1.  **(Optionnel) Peuplez la base de données avec des données fraîches :**
    ```bash
    bash run_scripts.sh
    ```

2.  **Lancez le serveur Backend (API FastAPI) :**
    *Ouvrez un premier terminal :*
    ```bash
    uvicorn api.app:app --reload --port 8001
    ```
    - API accessible sur `http://127.0.0.1:8001`.
    - Documentation sur `http://127.0.0.1:8001/docs`.

3.  **Lancez le serveur Frontend (Application Django) :**
    *Ouvrez un second terminal :*
    ```bash
    python manage.py runserver
    ```
    - Tableau de bord accessible sur `http://127.0.0.1:8000/`.

## ✅ Lancer les Tests

Les tests sont conçus pour s'exécuter dans un environnement isolé avec une base de données SQLite temporaire.

1.  **Préparez la base de données de test :**
    ```bash
    python tests/setup_test_db.py
    ```

2.  **Lancez les tests avec pytest :**
    ```bash
    pytest
    ```

## 📂 Structure du Projet

```
.
├── .github/workflows/ci.yml    # Workflow d'intégration et de déploiement continus
├── api/
│   └── app.py                  # Logique du backend API FastAPI (compatible PostgreSQL/SQLite)
├── dashboard/                    # Projet Django principal
├── viewer/                       # Application Django pour le frontend
│   ├── templates/
│   └── views.py                # Logique des vues (consommation de l'api)
├── data/                         # Fichiers de BDD SQLite (pour dev local)
├── docs/                         # Documentation (architecture, benchmark IA, rapports...)
├── scripts/                      # Scripts d'extraction et d'analyse
│   ├── extraction_news.py      # Extraction des actualités via Flux RSS
│   ├── llm_analyzer.py         # Logique d'appel à l'ia Gemini
│   └── stockage.py             # Gestion de la BDD (compatible PostgreSQL/SQLite)
├── tests/                        # Tests automatisés
│   ├── setup_test_db.py        # Création de la BDD de test SQLite
│   └── test_api.py             # Tests d'intégration pour l'api (avec injection de dépendances)
├── .env.example                # Fichier d'exemple pour les variables d'environnement
├── dockerfile                  # Instructions pour construire l'image Docker de l'api
├── deploy.sh                   # Script de déploiement exécuté sur le VPS
└── requirements.txt            # Dépendances Python du projet
```