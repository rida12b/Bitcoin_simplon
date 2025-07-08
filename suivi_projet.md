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
- [ ] **Tâche 1.1 (C1, C3) :** Développer le script de collecte des prix (`extraction_api.py`).
- [ ] **Tâche 1.2 (C1, C3) :** Développer le script de collecte des news (`extraction_news.py`).
- [ ] **Tâche 1.3 (C4) :** Développer le script de création de la base de données (`stockage.py`).
- [ ] **Tâche 1.4 (C5) :** Développer les endpoints de base de l'API FastAPI (ceux sans IA).

### Phase 2 : Bloc de Compétences 2 (L'IA)
- [ ] **Tâche 2.1 (C6, C7, C8) :** Formaliser la veille et le benchmark de l'IA dans `/docs`.
- [ ] **Tâche 2.2 (C9) :** Développer le module `llm_analyzer.py` et les endpoints IA dans l'API.
- [x] **Tâche 2.3 (C11, C12) :** Implémenter le monitoring (logging) et les tests `pytest` pour le module IA.
- [x] **Tâche 2.4 (C13) :** Mettre en place la CI/CD de base avec GitHub Actions.

### Phase 3 : Bloc de Compétences 3 (L'Application)
- [ ] **Tâche 3.1 (C14, C15, C16) :** Concevoir l'application Django (modèles, vues, URLs).
- [ ] **Tâche 3.2 (C17) :** Développer le frontend (templates HTML, CSS) en consommant l'API.
- [x] **Tâche 3.3 (C18, C19) :** Ajouter les tests d'API à la CI/CD.
- [ ] **Tâche 3.4 (C20, C21) :** Mettre en place la journalisation côté Django et documenter un incident simulé.

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

## 3. Journal des Modifications

- **[Date] :**
    - **Action :** Initialisation du projet. Création de l'arborescence et des fichiers de suivi `PLAN_PROJET_RNCP.md` et `suivi_projet.md`.
    - **Décision :** Choix d'une architecture découplée FastAPI/Django pour bien séparer les responsabilités et couvrir les blocs de compétences.

- **[Décembre 2024] :**
    - **Action :** Mise en place complète des tests automatisés (C12, C18) et de l'intégration continue (C13, C19).
    - **Décision :** Adoption du mocking pour les tests d'IA et création d'une base de données de test séparée.
    - **Refactorisation :** Amélioration de la testabilité du module `stockage.py` par injection de dépendances.

---

## 4. Suivi des Erreurs

| Date | Erreur Rencontrée | Cause Analysée | Solution Apportée | Compétence Testée (ex: C21) |
|------|-------------------|----------------|-------------------|-----------------------------|
| Décembre 2024 | `ModuleNotFoundError: No module named 'httpx'` lors de l'exécution du workflow GitHub Actions | Dépendance `httpx` installée en local mais absente du fichier `requirements.txt` | Ajout de `httpx` dans `requirements.txt` et nouveau commit. Workflow passé au vert. | C13, C19 - Démonstration de l'utilité de la CI pour détecter les problèmes de reproductibilité |

---

## 5. Architecture du Projet (Schéma Textuel)

```
[Utilisateur] -> [Navigateur] -> [Frontend: Django] --(Appel HTTP)--> [Backend: FastAPI] --(Appel API)--> [Google Gemini]
                                       ^                                       |
                                       |                                       v
                                       +----------------------------------> [Base de Données: SQLite]
```

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