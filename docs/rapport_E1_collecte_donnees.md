# Rapport de Mise en Situation E1 - Bloc 1

**Candidat :** Ridab
**Date :** 2024-06-07

---

## 1. Contexte et Objectifs du Projet (Compétences C14, C15)

*Cette section est une introduction. Elle explique au jury le "pourquoi" de votre projet.*

**Mon objectif pour cette section :**
> *Rédigez 1 ou 2 phrases pour répondre à chaque question. Soyez clair et concis.*

- **Quel est l'objectif principal de l'application "Bitcoin Analyzer" ?**
  > L'objectif principal de l'application "Bitcoin Analyzer" est de collecter automatiquement les données de prix et les actualités du Bitcoin, puis de les analyser et de les mettre à disposition via une API, afin de fournir des insights pertinents à des utilisateurs intéressés par la cryptomonnaie.

- **Quel problème ce projet cherche-t-il à résoudre ?**
  > Ce projet vise à centraliser et fiabiliser l'accès à l'information sur le Bitcoin, en automatisant la collecte et l'analyse des données, pour permettre à l'utilisateur d'obtenir rapidement des analyses et des tendances sans avoir à consulter plusieurs sources manuellement.

---

## 🟢 Journal d'Avancement - Bloc E1 (Compétences C1 à C4)

**Date :** 2024-07-29
**Auteur :** Ridab

### E1 - C1, C2, C3 : Collecte et Préparation des Données

- **Extraction automatisée (C1)** :
  - Script `extraction_api.py` développé pour interroger l'API Coinalyze et récupérer les prix horaires du Bitcoin sur 24h.
  - Fonction `get_bitcoin_data()` : gestion de la connexion, récupération, validation du format des données.
  - Gestion des erreurs d'API (affichage si échec).

- **Nettoyage et formatage (C3)** :
  - Transformation des données brutes en liste de dictionnaires structurés (timestamp, open, high, low, close, volume).
  - Vérification de la conformité du format avant insertion.

### E1 - C4 : Stockage Sécurisé des Données

- **Module `stockage.py`** :
  - Fonction `init_db()` : création automatique de la base SQLite et de la table `bitcoin_prices` (unicité sur le timestamp).
  - Fonction `insert_many()` : insertion en masse, évite les doublons.
  - Séparation claire extraction/stockage (modularité, robustesse).

- **Sécurité & bonnes pratiques** :
  - Utilisation de variables d'environnement pour la clé API (fichier `.env`).
  - Code documenté et testé en local (24 lignes insérées sans erreur).

### ✅ Validation de l'étape

- Chaîne extraction → stockage testée et fonctionnelle.
- Documentation mise à jour pour chaque étape.
- Prêt pour la suite : mise à disposition via API (FastAPI, compétence C5).

---

## 🟢 Journal d'Avancement - Bloc E1 (Compétence C5)

**Date :** 2024-07-29
**Auteur :** Ridab

### E1 - C5 : Mise à disposition des données via API REST (FastAPI)

- **Création de l'API FastAPI** :
  - Dossier `api/` créé, fichier `app.py` initialisé.
  - Installation des dépendances : `fastapi`, `uvicorn`.
  - Premier endpoint `/health` pour vérifier le bon fonctionnement de l'API.

- **Endpoint `/latest-price`** :
  - Permet de récupérer le dernier prix du Bitcoin stocké dans la base SQLite.
  - Lecture directe dans la table `bitcoin_prices`.

- **Endpoint `/price-history`** :
  - Permet de récupérer l'historique des prix (par défaut sur 24h, paramètre `limit` possible).
  - Retourne une liste structurée (timestamp, open, high, low, close, volume).

- **Tests et validation** :
  - Accès et test des endpoints via navigateur et Swagger UI (`/docs`).
  - Vérification de la conformité au référentiel (C5 : API REST fonctionnelle, documentation automatique, accès sécurisé à venir).

- **Préparation de la suite** :
  - Prochaine étape : ajout des endpoints pour les actualités Bitcoin et intégration de l'IA (Gemini).

---

## 🟢 Journal d'Avancement - Bloc E1 (Compétence C5, multi-source)

**Date :** 2024-07-29
**Auteur :** Ridab

### E1 - C5 : Intégration des actualités Bitcoin dans l'API FastAPI

- **Création de la table `bitcoin_news` et du script de scraping** :
  - Script `extraction_news.py` développé pour extraire les titres, liens et contenus des dernières actualités Bitcoin sur bitcoinmagazine.com.
  - Utilisation de BeautifulSoup et gestion des headers pour contourner les protections anti-bot.
  - Stockage automatisé dans la table `bitcoin_news` (unicité sur le titre, gestion des doublons).

- **Ajout du endpoint `/latest-news` dans FastAPI** :
  - Endpoint développé pour exposer les dernières actualités stockées dans la base SQLite.
  - Paramètre `limit` pour ajuster le nombre de news retournées.
  - Lecture directe dans la table, formatage JSON pour l'API.

- **Tests et validation** :
  - Accès et test du endpoint via navigateur et Swagger UI (`/docs`).
  - Vérification de la conformité au référentiel (C5 : API REST multi-source, documentation automatique, robustesse).

- **Préparation de la suite** :
  - Possibilité d'ajouter d'autres endpoints (historique, recherche, etc.).
  - Préparation à l'intégration de l'IA (Gemini) pour l'analyse des données.

---

## 🟠 Suivi des Erreurs et Gestion des Incidents - Bloc E1 (Compétence C21)

**Date :** 2024-07-29
**Auteur :** Ridab

### Incident technique : "no such table: bitcoin_prices" lors de l'appel à l'API

**Contexte**
- Lors des appels aux endpoints de l'API FastAPI qui nécessitent un accès à la base de données (ex: `/price-history`), une erreur 500 "Internal Server Error" était retournée.
- Après avoir ajouté une gestion des exceptions (`try...except`) dans le code de l'endpoint, le message d'erreur précis a pu être capturé : `sqlite3.OperationalError: no such table: bitcoin_prices`.

**Diagnostic**
- Le endpoint `/health` fonctionnait, confirmant que le serveur FastAPI lui-même était opérationnel.
- L'erreur indiquait clairement que l'application API, au moment de son exécution, ne trouvait pas la table `bitcoin_prices` dans le fichier de base de données qu'elle ciblait.
- **Hypothèse principale :** Les scripts d'extraction (`extraction_api.py`) et l'application API (`api/app.py`) n'utilisent pas le même contexte d'exécution. La fonction `init_db()` qui crée les tables a été exécutée par les scripts, mais jamais par le processus de l'API. L'API démarre et tente de lire une base de données qui, de son point de vue, est vide ou n'a pas les bonnes tables.

**Résolution**
- La solution consiste à s'assurer que la base de données et ses tables sont initialisées **au démarrage de l'application FastAPI elle-même**.
- Il faut importer la fonction `init_db()` dans `api/app.py` et l'appeler grâce à un événement de démarrage (`@app.on_event("startup")`).
- Cette approche garantit que, quel que soit le contexte d'exécution, l'API s'assure que la structure de la base de données est en place avant de commencer à accepter des requêtes.

**Leçon apprise**
- Une application (comme une API) et des scripts externes (comme des tâches d'extraction) ont des contextes d'exécution distincts. Il est crucial de ne pas supposer qu'une initialisation faite par l'un sera disponible pour l'autre.
- Les applications doivent gérer leur propre initialisation (connexions, création de BDD, etc.) pour être autonomes et robustes.
- La journalisation et la gestion précise des exceptions sont non-négociables pour un diagnostic rapide.

---

## 2. Phase 1 : Collecte et Stockage des Données

### 2.1. Automatisation de l'Extraction des Prix (Compétence C1)

*Cette section concerne le script `extraction_api.py` que vous venez de réaliser.*

**Mon objectif pour cette section :**
> *Décrivez précisément votre travail technique.*

- **Quelle source de données avez-vous choisie pour les prix du Bitcoin et pourquoi ?**
  > J'ai choisi l'API de Coinalyze car elle fournit des données OHLCV (Open, High, Low, Close, Volume) granulaires et fiables sur le Bitcoin, ce qui est essentiel pour réaliser des analyses financières précises et automatisées. Cette API est reconnue pour sa stabilité et sa documentation claire.

- **Décrivez le script `scripts/extraction_api.py`. Quel est son rôle ?**
  > Le script `extraction_api.py` est un script Python qui se connecte à l'API Coinalyze, prépare une requête HTTP GET avec les bons paramètres (symbole, intervalle, période), et récupère les données de prix du Bitcoin sur les dernières 24 heures. Il affiche les données reçues et gère les éventuelles erreurs de connexion.

- **Comment avez-vous géré les informations sensibles comme la clé d'API ? (Critère de sécurité C4/C5)**
  > Pour garantir la sécurité, la clé API n'est jamais écrite en dur dans le code. Elle est stockée dans un fichier `.env` qui est ignoré par Git grâce au fichier `.gitignore`. Le script utilise la librairie `python-dotenv` pour charger la clé en mémoire de façon sécurisée lors de l'exécution.

- **Comment votre script gère-t-il les erreurs de connexion à l'API ? (Critère de robustesse C1)**
  > Le script vérifie le code de statut de la réponse HTTP. Si le code est `200`, il traite les données normalement. Pour tout autre code (ex : 404, 500), il affiche un message d'erreur explicite avec le code et le texte de la réponse, puis retourne `None` pour éviter que le programme ne plante.

**Extrait de code pertinent :**
> *Copiez-collez ici votre fonction `get_bitcoin_data()` pour illustrer vos propos.*

```python
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
```

### 2.2. Plan de Stockage des Données (Compétences C2, C4)

*Cette section prépare le travail que nous allons faire juste après. Elle montre au jury que vous anticipez les prochaines étapes.*

**Mon objectif pour cette section :**
> *Décrivez la solution que vous allez mettre en place.*

- **Quelle technologie de base de données avez-vous choisie pour stocker les données et pourquoi ?**
  > Pour cette première phase, j'ai choisi SQLite. C'est une base de données légère, basée sur un fichier, qui ne nécessite pas de serveur dédié. Elle est idéale pour le développement local et la simplicité de mise en place du projet, tout en assurant la persistance des données.

- **Décrivez la structure de la table que vous allez créer (`bitcoin_prices`). Quelles seront les colonnes et leurs types ?**
  > La table `bitcoin_prices` contiendra les colonnes suivantes : `id` (INTEGER, PRIMARY KEY), `timestamp` (INTEGER, UNIQUE), `open` (REAL), `high` (REAL), `low` (REAL), `close` (REAL), `volume` (REAL). Le champ `timestamp` sera unique pour éviter les doublons lors de l'insertion des données.

--- 