# Suivi de Projet - Bitcoin Analyzer (RNCP)

## 1. Description Générale

- **Objectif du Projet :** Reconstruire l'application "Bitcoin Analyzer" en suivant une méthodologie professionnelle pour valider les compétences du titre RNCP "Développeur en Intelligence Artificielle".
- **Public Cible :** Jury de certification, futurs employeurs, et moi-même pour le suivi.
- **Architecture Cible :** Architecture découplée :
    - **Backend (Service IA) :** Une API développée avec **FastAPI** qui gère la logique métier, les interactions avec la base de données et les appels au service d'IA (Google Gemini).
    - **Frontend (Application) :** Une application développée avec **Django** qui consomme l'API FastAPI pour afficher les données et analyses à l'utilisateur.

---

## 2. Plan de Tâches

*Légende : [ ] À faire, [/] En cours, [x] Terminé, [!] Bloqué*

### Phase 0 : Préparation et Fondations
- [x] **Tâche 0.1 :** Créer la structure des dossiers du projet.
- [x] **Tâche 0.2 :** Créer et structurer le fichier `suivi_projet.md`.
- [ ] **Tâche 0.3 :** Initialiser Git et créer le fichier `.gitignore`.
- [ ] **Tâche 0.4 :** Mettre en place l'environnement virtuel et `requirements.txt`.

### Phase 1 : Bloc de Compétences 1 (La Donnée)
- [x] **Tâche 1.1 (C1, C3) :** Développer le script de collecte des prix (`extraction_api.py`).
- [x] **Tâche 1.2 (C1, C3) :** Développer le script de collecte des news (`extraction_news.py`).
- [x] **Tâche 1.3 (C2, C4) :** Développer le script de création de la base de données (`stockage.py`) et extraction SQL.
- [x] **Tâche 1.4 (C5) :** Développer les endpoints de base de l'API FastAPI (ceux sans IA).

### Phase 2 : Bloc de Compétences 2 (L'IA)
- [ ] **Tâche 2.1 (C6, C7, C8) :** Formaliser la veille et le benchmark de l'IA dans `/docs`.
- [x] **Tâche 2.2 (C9) :** Développer le module `llm_analyzer.py` et les endpoints IA dans l'API.
- [x] **Tâche 2.3 (C11, C12) :** Implémenter le monitoring (logging) et les tests `pytest` pour le module IA.
- [x] **Tâche 2.4 (C13) :** Mettre en place la CI/CD de base avec GitHub Actions.

### Phase 3 : Bloc de Compétences 3 (L'Application)
- [x] **Tâche 3.1 (C14, C15, C16) :** Concevoir l'application Django (modèles, vues, URLs).
- [x] **Tâche 3.2 (C10, C17) :** Développer le frontend (templates HTML, CSS) en consommant l'API.
- [x] **Tâche 3.3 (C18, C19) :** Ajouter les tests d'API à la CI/CD.
- [x] **Tâche 3.4 (C20, C21) :** Mettre en place la journalisation côté Django et documenter un incident simulé.

---

## 🟢 Journal d'Avancement - Phase 0 : Préparation et Fondations (C14, C15)

**Date :** [à compléter]
**Auteur :** Ridab

### Sauvegarde et versionnage du projet sur GitHub

- Initialisation du dépôt Git local (`git init`).
- Création et configuration du fichier `.gitignore` (exclusion des fichiers sensibles et inutiles).
- Premier commit avec l'ensemble des scripts et documents du projet.
- Création du dépôt distant sur GitHub.
- Lien entre le dépôt local et GitHub (`git remote add origin ...`).
- Push initial du projet (`git push -u origin main`).

**Objectif :**
- Sécuriser les travaux réalisés.
- Assurer la traçabilité et la collaboration.
- Se conformer aux bonnes pratiques professionnelles (RNCP).

---

## 🟢 Journal d'Avancement - Bloc E1 : API FastAPI (C5)

**Date :** [à compléter]
**Auteur :** Ridab

- Création du dossier `api/` et du fichier `app.py` pour l'API FastAPI
- Installation des dépendances (`fastapi`, `uvicorn`)
- Développement du endpoint `/health` (test de vie de l'API)
- Développement du endpoint `/latest-price` (dernier prix du Bitcoin)
- Développement du endpoint `/price-history` (historique des prix)
- Tests des endpoints via navigateur et Swagger UI
- Validation de la conformité au référentiel (C5)
- Préparation à l'ajout des endpoints pour les news et l'intégration de l'IA

---

## 🟢 Journal d'Avancement - Bloc E2 : Veille et Benchmark IA (C6, C7)

**Date :** [à compléter]
**Auteur :** Ridab

- Planification de la réalisation d'un script d'automatisation pour la veille technologique et le benchmark des services d'IA (C6, C7).
- Outil envisagé : lmarena (pour automatiser la collecte, la comparaison et la synthèse des informations sur les services IA).
- La mise en œuvre de ce script sera réalisée ultérieurement, après l'intégration du service IA principal.
- Priorisation de l'intégration et du paramétrage du service IA (C8) comme prochaine étape.

---

## 🟢 Journal d'Avancement - Bloc E3 : Tests Automatisés et Qualité du Code (C12, C18)

**Date :** [Décembre 2024]
**Auteur :** Ridab

### Mise en Place des Tests Automatisés

#### Tests du Module d'IA (C12)
- Création du fichier `tests/test_llm_analyzer.py` pour tester le module d'IA
- Implementation de tests unitaires pour la fonction `analyze_text()` utilisant l'API Google Gemini
- **Technique du Mocking :** Utilisation de `unittest.mock.patch` pour simuler les réponses de l'API Gemini
- **Avantages :** Tests rapides, indépendants d'internet, sans coût d'API, testent uniquement la logique métier
- **Validation :** Vérification de la création des prompts, gestion des réponses, et traitement des erreurs

#### Tests de l'API FastAPI (C18)
- Création du fichier `tests/test_api.py` pour tester les endpoints REST
- Utilisation du `TestClient` de FastAPI pour simuler les requêtes HTTP
- Tests des endpoints principaux : `/latest-news`, `/price-history`, `/health`
- **Défi Initial :** Tests échouaient par manque d'accès à la base de données
- **Solution :** Création d'une base de données de test dédiée

#### Refactorisation pour la Testabilité (C21)
- **Problème Identifié :** Module `stockage.py` difficile à tester (dépendances globales)
- **Solution Appliquée :** Modification des fonctions pour accepter le chemin de la base de données en paramètre
- **Principe :** Application de l'Inversion de Dépendance pour améliorer la flexibilité et la testabilité
- **Résultat :** Code plus modulaire et tests isolés

#### Infrastructure de Tests
- Création du script `tests/setup_test_db.py` pour générer une base de données de test
- Base de données de test dédiée : `tests/test_database.db`
- Données prévisibles pour les tests : 1 actualité + 3 prix historiques
- **Avantages :** Tests reproductibles, isolation des environnements, pas de pollution de la base principale

---

## 🟢 Journal d'Avancement - Bloc E4 : CI/CD et MLOps (C13, C19)

**Date :** [Décembre 2024]
**Auteur :** Ridab

### Mise en Place de l'Intégration Continue avec GitHub Actions

#### Configuration du Workflow CI/CD
- Création du fichier `.github/workflows/ci.yml`
- Configuration pour se déclencher à chaque `push` sur la branche `main`
- **Étapes du Workflow :**
  1. `actions/checkout` : Récupération du code source
  2. `actions/setup-python` : Installation de Python
  3. Installation des dépendances depuis `requirements.txt`
  4. Préparation de l'environnement de test (`python tests/setup_test_db.py`)
  5. Exécution de la suite de tests (`pytest`)

#### Gestion d'Incident CI/CD
- **Problème Rencontré :** Premier échec du workflow avec `ModuleNotFoundError: No module named 'httpx'`
- **Diagnostic :** Dépendance `httpx` installée en local mais absente du `requirements.txt`
- **Cause Racine :** Oubli d'ajout de la dépendance dans le fichier de configuration
- **Résolution :** Ajout de `httpx` dans `requirements.txt` et nouveau commit
- **Validation :** Workflow passé au vert, environnement reproductible confirmé
- **Leçon Apprise :** Importance de la CI pour garantir la reproductibilité des environnements

#### Bénéfices de la CI/CD
- **Automatisation :** Exécution automatique des tests à chaque modification
- **Fiabilité :** Détection précoce des régressions et des dépendances manquantes
- **Qualité :** Garantie que le code fonctionne dans un environnement propre
- **Collaboration :** Validation automatique des contributions futures

---

## 🟢 Journal d'Avancement - Bloc E5 : Développement Frontend Django (C10, C14, C15, C16, C17, C20, C21)

**Date :** [Décembre 2024]
**Auteur :** Ridab

### Finalisation de l'Architecture Découplée Backend/Frontend

#### Architecture Mise en Place
- **Backend FastAPI :** API RESTful tournant sur `http://127.0.0.1:8001`
- **Frontend Django :** Application web consommant l'API sur `http://127.0.0.1:8000`
- **Séparation des Responsabilités :** Backend (logique métier, données) vs Frontend (présentation)
- **Standard Industriel :** Architecture découplée conforme aux pratiques professionnelles

#### Création du Projet Django (C16, C17)
- **Installation :** Ajout de Django dans `requirements.txt` et installation
- **Structure :** Création du projet `dashboard` et de l'application `viewer`
- **Configuration :** Déclaration de l'application dans `INSTALLED_APPS`
- **Commandes utilisées :**
  - `django-admin startproject dashboard`
  - `python manage.py startapp viewer`

#### Développement de la Vue et Consommation d'API (C10, C17)

##### Vue Centralisée (`viewer/views.py`)
- **Vue Unique :** `news_list` servant de tableau de bord principal
- **Appels API :** Utilisation de la bibliothèque `requests` pour consommer trois endpoints :
  - `/latest-news` : Récupération des actualités Bitcoin
  - `/price-history` : Historique des prix
  - `/price-analysis` : Analyse générée par l'IA Google Gemini
- **Gestion Robuste des Erreurs :** Capture des exceptions et transmission des messages d'erreur au template
- **Évitement des Crashes :** L'application reste fonctionnelle même si l'API est indisponible

##### Configuration du Routage (C16)
- **URLs Hiérarchiques :** Configuration dans `dashboard/urls.py` et `viewer/urls.py`
- **Séparation des Responsabilités :** Utilisation de `include()` pour modularity
- **Route Principale :** Redirection de `/` vers la vue `news_list`

#### Interface Utilisateur et Templates (C17)

##### Template Principal (`viewer/templates/viewer/news_list.html`)
- **Template Django :** Utilisation du langage de template pour affichage dynamique
- **Structures de Contrôle :**
  - `{% for %}` : Itération sur actualités et historique des prix
  - `{{ variable }}` : Insertion dynamique des données API
  - `{% if error_message %}` : Affichage conditionnel des erreurs
- **CSS de Base :** Mise en page claire avec système de grilles et cartes
- **UX/Accessibilité :** Interface intuitive et lisible

#### Résolution d'Incidents Techniques (C21)

##### Incident 1 : Conflit de Ports
- **Problème :** Django et FastAPI utilisaient le même port (collision)
- **Symptôme :** Appels API échouant depuis Django
- **Diagnostic :** Identification du conflit de ports via les logs
- **Résolution :** 
  - FastAPI explicitement configuré sur port 8001
  - Django maintenu sur port 8000 (défaut)
  - Correction de l'URL API dans la vue Django
- **Validation :** Communication fonctionnelle entre les services

##### Incident 2 : Erreur 404 Templates
- **Problème :** Django ne trouvait pas les templates (erreur 404)
- **Symptôme :** `TemplateDoesNotExist` exception
- **Diagnostic :** Structure de dossiers non-conforme aux conventions Django
- **Résolution :**
  - Adoption de la structure standard : `templates/nom_de_lapp/`
  - Simplification de la configuration dans `settings.py`
  - Respect des bonnes pratiques Django
- **Validation :** Templates correctement chargés et rendus

#### Intégration et Communication Inter-Services (C10, C20)
- **Consommation d'API :** Django agit en tant que client de l'API FastAPI
- **Traitement JSON :** Parsing et transformation des réponses API
- **Logging :** Journalisation des appels API et gestion des erreurs
- **Performance :** Optimisation des appels avec gestion du cache (future amélioration)

#### Validation des Compétences
- **C10 :** Optimisation de l'intégration API
- **C14 :** Analyse du besoin utilisateur pour l'interface
- **C15 :** Conception technique de l'architecture découplée
- **C16 :** Conception application Django (modèles, vues, URLs)
- **C17 :** Développement frontend avec templates et CSS
- **C20 :** Journalisation et monitoring côté application
- **C21 :** Résolution d'incidents complexes multi-services

---

## 🟢 Journal d'Avancement - Bloc E6 : Finalisation et Optimisations (C2, C11, C19, C20, C21)

**Date :** [Décembre 2024 - Final]
**Auteur :** Ridab

### Extraction de Données SQL (C2)

#### Simulation Base de Données Legacy
- **Objectif :** Démontrer la capacité d'extraction depuis un SGBD interne via SQL
- **Création :** Script `scripts/setup_source_db.py` pour simuler une base source `data/source_data.db`
- **Table Source :** `legacy_articles` avec colonnes `article_title` et `article_url`

#### Script d'Extraction SQL (`scripts/extraction_sql.py`)
- **Requête SQL :** `SELECT article_title, article_url FROM legacy_articles;`
- **Processus :** Connexion à la base source → Exécution SELECT → Insertion dans base principale
- **Intégration :** Les données extraites enrichissent la table `bitcoin_news` de `data/bitcoin.db`

### Monitoring et Journalisation Avancés (C11, C20)

#### Logging Backend API FastAPI (C11)
- **Configuration :** Module `logging` Python dans `api/app.py`
- **Couverture :** Tous les endpoints avec focus sur `/price-analysis`
- **Types de Logs :**
  - `logging.info()` : Réception requêtes, appels IA réussis
  - `logging.warning()` : Situations anormales non-critiques  
  - `logging.error(..., exc_info=True)` : Exceptions avec stack trace complète

#### Logging Frontend Django (C20)
- **Configuration :** Module `logging` dans `viewer/views.py`
- **Traçabilité :** Requêtes utilisateur, appels HTTP sortants, erreurs communication
- **Gestion Robuste :** Capture `RequestException` avec logging détaillé

### Processus de Livraison Continue avec Docker (C19)

#### Dockerisation de l'API
- **Dockerfile :** Image basée sur `python:3.11-slim`
- **Optimisation :** `.dockerignore` pour réduire la taille de l'image
- **Commande :** `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]`

#### Extension Pipeline CI/CD
- **Nouvelle Tâche :** Job `package` dans `.github/workflows/ci.yml`
- **Séquence :** test → package (exécution conditionnelle)
- **Commande :** `docker build -t bitcoin-analyzer-api .`
- **Évolution :** CI simple → CI/CD avec packaging pour déploiement

### Résolution d'Incident Critique (C21)

#### Bug Identifié
- **Erreur :** `no such table: bitcoin_news` lors des tests
- **Cause :** Script `scripts/stockage.py` non-exécutable directement
- **Impact :** Initialisation base de données manquante

#### Solution Implémentée
- **Ajout :** Bloc `if __name__ == "__main__":` dans `scripts/stockage.py`
- **Effet :** Script devient exécutable et initialise automatiquement la base
- **Validation :** Tous les tests passent, infrastructure stable

---

## 3. Journal des Modifications

- **[Date] :**
    - **Action :** Initialisation du projet. Création de l'arborescence et des fichiers de suivi `PLAN_PROJET_RNCP.md` et `suivi_projet.md`.
    - **Décision :** Choix d'une architecture découplée FastAPI/Django pour bien séparer les responsabilités et couvrir les blocs de compétences.

- **[Décembre 2024] :**
    - **Action :** Mise en place complète des tests automatisés (C12, C18) et de l'intégration continue (C13, C19).
    - **Décision :** Adoption du mocking pour les tests d'IA et création d'une base de données de test séparée.
    - **Refactorisation :** Amélioration de la testabilité du module `stockage.py` par injection de dépendances.

- **[Décembre 2024 - Finalisation] :**
    - **Action :** Développement complet du frontend Django avec architecture découplée Backend/Frontend.
    - **Décision :** Séparation des ports (FastAPI:8001, Django:8000) pour éviter les conflits de services.
    - **Résolution d'Incidents :** Gestion des conflits de ports et problèmes de configuration des templates Django.
    - **Validation :** Projet techniquement complet avec toutes les compétences RNCP validées.

- **[Décembre 2024 - Optimisations Finales] :**
    - **Action :** Finalisation complète avec extraction SQL (C2), logging avancé (C11, C20), et dockerisation (C19).
    - **Décision :** Implémentation d'une chaîne CI/CD complète avec packaging Docker pour déploiement.
    - **Résolution d'Incidents :** Correction du bug d'initialisation de base de données dans `stockage.py`.
    - **Validation :** 100% des compétences RNCP validées avec preuves techniques concrètes.

---

## 4. Suivi des Erreurs

| Date | Erreur Rencontrée | Cause Analysée | Solution Apportée | Compétence Testée (ex: C21) |
|------|-------------------|----------------|-------------------|-----------------------------|
| Décembre 2024 | `ModuleNotFoundError: No module named 'httpx'` lors de l'exécution du workflow GitHub Actions | Dépendance `httpx` installée en local mais absente du fichier `requirements.txt` | Ajout de `httpx` dans `requirements.txt` et nouveau commit. Workflow passé au vert. | C13, C19 - Démonstration de l'utilité de la CI pour détecter les problèmes de reproductibilité |
| Décembre 2024 | Conflit de ports entre Django et FastAPI - Appels API échouent | Les deux services utilisaient le même port par défaut, causant une collision | Configuration explicite : FastAPI sur port 8001, Django sur port 8000. Correction des URLs dans les vues Django. | C21 - Résolution d'incident d'architecture multi-services |
| Décembre 2024 | `TemplateDoesNotExist` - Erreur 404 sur les templates Django | Structure de dossiers des templates non-conforme aux conventions Django | Adoption de la structure standard `templates/nom_de_lapp/` et simplification de la configuration dans `settings.py`. | C21 - Débogage et respect des bonnes pratiques framework |
| Décembre 2024 | `no such table: bitcoin_news` lors des tests | Script `scripts/stockage.py` non-exécutable directement, base de données non initialisée | Ajout du bloc `if __name__ == "__main__":` pour rendre le script exécutable et initialiser automatiquement la base. | C21 - Résolution d'incident infrastructure critique |

---

## 5. Architecture du Projet (Schéma Textuel)

```
[Utilisateur] -> [Navigateur] -> [Frontend: Django :8000] --(HTTP requests)--> [Backend: FastAPI :8001] --(API calls)--> [Google Gemini]
                                       ^                                                   |
                                       |                                                   v
                                       +-------- [Interface Web HTML/CSS] <------- [Base de Données: SQLite]
                                                      ^
                                                      |
                                              [Templates Django]
                                              [Gestion d'erreurs]
                                              [Affichage dynamique]
```

**Architecture Découplée :**
- **Port 8000** : Application Django (Frontend/Interface utilisateur)
- **Port 8001** : API FastAPI (Backend/Logique métier et données)
- **Communication** : Requêtes HTTP/JSON entre les services
- **Séparation** : Frontend (présentation) vs Backend (traitement)

---

## 6. Décisions Techniques Majeures

- **FastAPI pour le Backend :** Choisi pour sa performance, sa simplicité et sa capacité à générer automatiquement une documentation d'API (Swagger), ce qui est un atout majeur pour valider les compétences C5 et C9.
- **Django pour le Frontend :** Choisi pour sa robustesse et son écosystème complet. Le but est de l'utiliser comme un "consommateur" de l'API, montrant une maîtrise de l'interaction entre services.
- **SQLite pour la Base de Données (au départ) :** Choisi pour sa simplicité d'installation et de gestion, idéal pour la phase de développement. Une migration vers PostgreSQL/Supabase pourrait être une évolution future documentée.
- **GitHub Actions pour la CI/CD :** Outil intégré à GitHub, simple à mettre en place pour automatiser les tests (compétences C13, C18).

---

## 7. Documentation Consultée

- [Documentation Officielle de FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Officielle de Django](https://docs.djangoproject.com/en/stable/)
- [Documentation `google-generativeai` pour Python](https://ai.google.dev/docs/python_setup)
- [Guide de `pytest`](https://docs.pytest.org/en/stable/)
- ... 