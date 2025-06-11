# Plan d'Action pour la Refonte du Projet "Bitcoin Analyzer" (Conformité RNCP)

## 🎯 Objectif Principal
Ce document vous sert de guide pour reconstruire votre projet étape par étape. L'objectif est de vous approprier chaque compétence du **`referenciel.md`** en appliquant une méthodologie de travail rigoureuse et documentée.

**Règle d'or :** Pour chaque étape, vous devez d'abord mettre à jour votre fichier `suivi_projet.md` pour planifier la tâche, puis la réaliser, et enfin documenter ce que vous avez fait et appris.

---

## Phase 0 : Préparation et Fondations (Essentiel)

Avant de coder, préparez le terrain. Une bonne structure est la clé de la réussite.

1.  **✅ Créer le `suivi_projet.md`**
    -   Créez ce fichier s'il n'est pas parfait. Il sera votre journal de bord.
    -   Inspirez-vous de la structure de celui dans `repomix-output.xml`, mais adaptez-le pour ce nouveau projet.
    -   **Sections à inclure :** Description, Plan de Tâches (To-Do, In Progress, Done), Journal des Modifications, Suivi des Erreurs, Architecture du Projet, Documentation Consultée, Décisions Techniques.

2.  **✅ Initialiser le Contrôle de Version avec Git**
    -   Créez un nouveau dépôt Git (`git init`).
    -   Créez un fichier `.gitignore` (vous pouvez réutiliser celui du `repomix`).
    -   Faites un premier commit : `git commit -m "Initialisation du projet et du plan d'action RNCP"`.

3.  **✅ Mettre en Place l'Environnement Virtuel**
    -   Créez un environnement virtuel Python : `python -m venv venv`.
    -   Activez-le.
    -   Créez un fichier `requirements.txt` vide pour le moment.

---

## Phase 1 : Bloc de Compétences 1 - La Donnée

**Objectif :** Mettre en place une chaîne de collecte, de stockage et de mise à disposition des données fiable et automatisée.

### Étape 1.1 : Collecte de Données (C1, C2, C3)
-   **Tâche :** Recréer les scripts `scripts/extraction_api.py` et `scripts/extraction_news.py`.
-   **Compétences visées :**
    -   **C1 :** Automatiser l'extraction (API Coinalyze, scraping de Bitcoin Magazine).
    -   **C3 :** Agréger et nettoyer. Même si c'est simple, prévoyez une fonction qui valide que les données reçues ont le bon format avant de les enregistrer.
-   **Points d'attention :**
    -   Gérez les erreurs (ex: que se passe-t-il si l'API ne répond pas ? Si la structure de la page web change ?).
    -   Documentez votre code pour expliquer ce que fait chaque fonction.
    -   Utilisez des variables d'environnement pour les informations sensibles (clés API) avec un fichier `.env` et `python-dotenv`.

### Étape 1.2 : Stockage des Données (C4)
-   **Tâche :** Créer le script `scripts/stockage.py` qui initialise la base de données. Pour commencer, restez sur SQLite pour sa simplicité.
-   **Compétences visées :**
    -   **C4 :** Créer la BDD. Pensez au modèle de données. Dessinez (même en texte) le schéma de vos tables `bitcoin_prices` et `bitcoin_news` dans votre `suivi_projet.md`.
    -   **RGPD :** Même si vous ne stockez pas de données personnelles, mentionnez dans votre documentation que vous avez conscience de cette problématique.
-   **Points d'attention :**
    -   Assurez-vous que vos scripts d'extraction appellent bien ce module pour stocker les données.
    -   La table doit avoir une contrainte d'unicité (par exemple sur le `timestamp` pour les prix ou le `titre` pour les news) pour éviter les doublons.

### Étape 1.3 : Mise à Disposition via une API (C5)
-   **Tâche :** Développer la première version de votre API avec FastAPI (`api/app.py`).
-   **Compétences visées :**
    -   **C5 :** Développer une API REST.
-   **Points d'attention :**
    -   Commencez par les *endpoints* qui ne nécessitent pas l'IA :
        -   `/health`
        -   `/latest-price`
        -   `/price-history`
        -   `/latest-news`
    -   Structurez bien votre code FastAPI.
    -   Documentez votre API directement dans le code avec les docstrings (FastAPI générera une documentation Swagger automatiquement).

---

## Phase 2 : Bloc de Compétences 2 - L'Intelligence Artificielle

**Objectif :** Intégrer un service d'IA pour enrichir les données et exposer ses fonctionnalités.

### Étape 2.1 : Veille et Sélection du Service (C6, C7, C8)
-   **Tâche :** Formaliser le choix de Google Gemini.
-   **Compétences visées :**
    -   **C6 :** Réaliser une veille. Créez une section "Veille Technologique" dans votre `suivi_projet.md` où vous listez les sources que vous avez consultées (docs Gemini, articles, etc.).
    -   **C7 :** Identifier et benchmarker des services. Reprenez le benchmark que vous aviez fait (Gemini vs OpenAI vs autres) et formalisez-le dans un document (ex: `docs/benchmark_ia.md`).
    -   **C8 :** Paramétrer le service. Assurez-vous que la configuration de Gemini (clé API) est bien gérée via les variables d'environnement.

### Étape 2.2 : Exposition du Modèle via l'API (C9)
-   **Tâche :** Ajouter les *endpoints* d'analyse à votre API FastAPI.
-   **Compétences visées :**
    -   **C9 :** Développer une API exposant un modèle d'IA.
-   **Points d'attention :**
    -   Créez le script `scripts/llm_analyzer.py` qui contiendra toute la logique d'appel à Gemini.
    -   Ajoutez les *endpoints* sécurisés à `api/app.py` :
        -   `/price-analysis`
        -   `/news-analysis`
        -   `/insights`
    -   Implémentez une authentification simple (ex: `Bearer Token`) comme dans le projet initial. La sécurité est un critère clé.

### Étape 2.3 : Monitoring et Tests du Modèle (C11, C12)
-   **Tâche :** Mettre en place le suivi et les tests pour la partie IA.
-   **Compétences visées :**
    -   **C11 :** Monitorer le modèle. Intégrez le `logging` dans votre API pour tracer les appels à Gemini: durée, succès/échec, nombre de tokens (approximatif).
    -   **C12 :** Programmer les tests automatisés. Créez un fichier `test/test_llm.py` et utilisez `pytest` et `unittest.mock` pour tester `llm_analyzer.py` **sans appeler réellement l'API Gemini**. C'est une compétence très appréciée.
-   **Points d'attention :**
    -   Testez que vos fonctions de formatage de prompt fonctionnent bien.
    -   Simulez ("mockez") les réponses de Gemini pour valider le comportement de votre code.

### Étape 2.4 : Chaîne de Livraison Continue (CI/CD) (C13)
-   **Tâche :** Mettre en place une CI simple avec GitHub Actions.
-   **Compétences visées :**
    -   **C13 :** Créer une chaîne de livraison continue.
-   **Points d'attention :**
    -   Créez le fichier `.github/workflows/ci.yml`.
    -   Le workflow doit :
        1.  Installer Python.
        2.  Installer les dépendances (`pip install -r requirements.txt`).
        3.  Lancer les tests (ceux de `test/test_llm.py` et les futurs tests d'API).

---

## Phase 3 : Bloc de Compétences 3 - L'Application

**Objectif :** Construire une application web complète, robuste et bien gérée, qui consomme l'API IA.

### Étape 3.1 : Conception de l'Application (C14, C15, C16)
-   **Tâche :** Planifier et documenter l'architecture de votre application Django.
-   **Compétences visées :**
    -   **C14 :** Analyser le besoin. Rédigez les "user stories" dans votre `suivi_projet.md`. (Ex: "En tant qu'utilisateur, je veux voir le dernier prix du Bitcoin sur la page d'accueil").
    -   **C15 :** Concevoir le cadre technique. Décrivez l'architecture (Django + API FastAPI) dans `suivi_projet.md`.
    -   **C16 :** Coordonner. Pour un projet solo, cela signifie suivre votre plan de tâches. Mettez à jour les statuts (`[ ]`, `[x]`) dans `suivi_projet.md`.

### Étape 3.2 : Développement du Frontend (C17)
-   **Tâche :** Construire l'application Django `viewer`.
-   **Compétences visées :**
    -   **C17 :** Développer les composants et interfaces.
-   **Points d'attention :**
    -   Créez le projet Django (`django-admin startproject dashboard`).
    -   Créez l'application (`python manage.py startapp viewer`).
    -   Dans `viewer/models.py`, recréez la classe `APIConnector` qui sera responsable des appels à votre API FastAPI.
    -   Créez les vues dans `viewer/views.py` et les templates HTML.
    -   Portez une attention particulière à l'accessibilité (attributs `alt` pour les images, labels pour les formulaires, etc.), c'est un critère du référentiel.

### Étape 3.3 : Tests et Déploiement Continus (C18, C19)
-   **Tâche :** Renforcer votre CI et préparer le déploiement.
-   **Compétences visées :**
    -   **C18 :** Automatiser les phases de test. Créez un fichier `test/test_api.py` pour tester les endpoints de votre API FastAPI. Ajoutez cette étape à votre workflow GitHub Actions.
    -   **C19 :** Créer un processus de livraison continue. Pour la certification, une CI qui teste et valide est déjà excellente. Vous pouvez ajouter une étape de "build" (ex: `docker build`) pour montrer que vous anticipez le déploiement.

### Étape 3.4 : Surveillance et Maintenance (C20, C21)
-   **Tâche :** Mettre en place la surveillance et la gestion des erreurs.
-   **Compétences visées :**
    -   **C20 :** Surveiller l'application. Ajoutez du logging dans l'application Django (ex: logguer quand un appel à l'API échoue).
    -   **C21 :** Résoudre les incidents. Créez une section "Suivi des Erreurs" dans `suivi_projet.md`. Si vous rencontrez un bug, documentez-le, expliquez comment vous l'avez résolu, et si possible, écrivez un test qui aurait pu l'intercepter.

---
## Derniers Conseils pour l'Examen

-   **Maîtrisez votre discours :** Soyez capable d'expliquer chaque choix technique en le reliant à une compétence du référentiel. Pourquoi FastAPI ? Pourquoi Django ? Pourquoi le mocking dans les tests ?
-   **La documentation est votre alliée :** Un projet bien documenté (dans le code, dans les commits, et dans `suivi_projet.md`) montre une grande maturité professionnelle.
-   **Simplicité > Complexité :** Un projet plus simple mais parfaitement maîtrisé, testé et documenté vaut mieux qu'un projet très complexe mais fragile.

Bon courage pour cette préparation, vous avez tous les éléments pour réussir ! 