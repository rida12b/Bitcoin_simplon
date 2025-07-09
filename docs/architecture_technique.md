# Architecture Technique - Bitcoin Analyzer


## 2. Schéma d'Architecture Détaillé


```mermaid
graph TD;
    subgraph "Utilisateur Final"
        U[👤 Alex, Investisseur]
    end

    subgraph "Frontend (Interface Utilisateur)"
        direction LR
        U -- "1. Requête HTTP (Port 8000)" --> D[Serveur Django];
        D -- "5. Renvoi de la page HTML" --> U;
    end

    subgraph "Backend (Service d'Analyse)"
        direction LR
        D -- "2. Appel API REST (Port 8001)" --> F[API FastAPI];
        F -- "3a. Requête SQL" --> DB[(🗃️ Base de Données SQLite)];
        DB -- " " --> F;
        F -- "3b. Appel API Externe" --> G[API Google Gemini];
        G -- " " --> F;
        F -- "4. Réponse JSON" --> D;
    end

    style D fill:#A9D0F5,stroke:#333,stroke-width:2px
    style F fill:#F5BCA9,stroke:#333,stroke-width:2px


**Description des flux :**
1.  L'utilisateur accède au tableau de bord via son navigateur, envoyant une requête au serveur **Django** sur le port 8000.
2.  La vue Django agit comme un client et envoie des requêtes HTTP à l'API **FastAPI** sur le port 8001 pour obtenir les données (news, prix, analyse).
3.  L'API FastAPI orchestre la récupération des données :
    a. Elle interroge la base de données **SQLite** pour les données de marché et les actualités.
    b. Elle appelle l'API externe de **Google Gemini** pour générer l'analyse de tendance.
4.  FastAPI agrège les réponses et les retourne au format **JSON** à Django.
5.  Django utilise ces données pour populer le template HTML et renvoie la page web complète au navigateur de l'utilisateur.

## 3. Pile Technologique et Justification des Choix

Chaque technologie a été sélectionnée après une analyse de ses forces et de sa pertinence pour le projet, en considérant également des alternatives.

### Langage : Python 3.11
*   **Justification :** Choix naturel pour un projet d'IA grâce à son écosystème mature (Pandas, Scikit-learn pour des évolutions futures) et ses excellentes bibliothèques pour le développement web (`fastapi`, `django`) et l'accès aux données (`requests`, `beautifulsoup4`). Sa syntaxe claire favorise un développement rapide et une maintenance aisée.

### Backend : FastAPI
*   **Justification :**
    *   **Haute Performance :** Basé sur Starlette et Pydantic, FastAPI est l'un des frameworks Python les plus rapides, idéal pour une API qui se doit d'être réactive.
    *   **Documentation Automatique (validation de C5) :** Génère nativement une documentation interactive (Swagger UI / OpenAPI), ce qui est un gain de temps majeur et une exigence de qualité professionnelle pour toute API.
    *   **Validation des Données :** Utilise Pydantic pour une validation robuste et claire des types de données en entrée et en sortie, réduisant ainsi les bugs.
*   **Alternative Écartée :**
    *   **Flask :** Bien que plus léger, Flask ne propose pas de validation de données ni de documentation automatique nativement. Les ajouter nécessiterait des bibliothèques tierces (ex: Flask-RESTful, Flasgger), complexifiant la maintenance et ajoutant des points de défaillance potentiels.
    *   **Django REST Framework (DRF) :** Très puissant mais plus lourd et plus complexe à configurer pour une API simple comme celle-ci. L'approche "tout-en-un" de DRF était superflue, FastAPI offrant un meilleur équilibre performance/simplicité pour ce projet.

### Frontend : Django
*   **Justification :**
    *   **Framework Complet ("Batteries included") :** Offre une structure robuste pour construire une application web complète avec un ORM, un système de templates puissant, et des fonctionnalités de sécurité intégrées.
    *   **Démonstration de Compétence :** Utiliser Django comme simple consommateur d'API démontre la maîtrise des architectures découplées, une compétence très recherchée dans le monde professionnel, qui valorise la séparation des responsabilités.
*   **Alternative Écartée :**
    *   **Streamlit/Gradio :** Ces outils sont excellents pour des prototypes rapides de data science et des interfaces de démonstration de modèles. Cependant, ils offrent moins de contrôle sur le design (HTML/CSS) et la structure de l'application, les rendant moins adaptés pour construire une application web personnalisable et évolutive destinée à un utilisateur final.

### Base de Données : SQLite
*   **Justification :**
    *   **Simplicité :** Aucune installation de serveur requise, la base de données est un simple fichier. C'est la solution parfaite pour le développement, les tests automatisés et un déploiement léger.
    *   **Intégration Python :** Fait partie de la bibliothèque standard de Python, ne nécessitant aucune dépendance externe pour fonctionner.
*   **Vision d'Évolution (Scalabilité) :** SQLite est suffisant pour la version 1 du projet. Pour une mise en production à plus grande échelle, l'architecture est pensée pour une migration future. Le code d'accès aux données étant bien isolé, il serait aisé de le remplacer par des appels à un SGBD plus robuste comme **PostgreSQL**. Cette anticipation démontre une réflexion sur le cycle de vie complet de l'application.

### Service d'IA : Google Gemini Pro
*   **Justification :** Le choix de ce modèle n'est pas arbitraire. Il est le résultat d'un benchmark formel documenté dans `docs/benchmark_ia.md`. Gemini Pro a été sélectionné car il offre le meilleur compromis entre :
    1.  **Performance :** Un score Elo très compétitif sur la LMSys Chatbot Arena.
    2.  **Coût :** Un tarif très abordable, rendant le projet économiquement viable.
    3.  **Facilité d'intégration :** Une bibliothèque Python officielle (`google-generativeai`) claire et bien documentée.