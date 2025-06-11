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
- [ ] **Tâche 2.3 (C11, C12) :** Implémenter le monitoring (logging) et les tests `pytest` pour le module IA.
- [ ] **Tâche 2.4 (C13) :** Mettre en place la CI/CD de base avec GitHub Actions.

### Phase 3 : Bloc de Compétences 3 (L'Application)
- [ ] **Tâche 3.1 (C14, C15, C16) :** Concevoir l'application Django (modèles, vues, URLs).
- [ ] **Tâche 3.2 (C17) :** Développer le frontend (templates HTML, CSS) en consommant l'API.
- [ ] **Tâche 3.3 (C18, C19) :** Ajouter les tests d'API à la CI/CD.
- [ ] **Tâche 3.4 (C20, C21) :** Mettre en place la journalisation côté Django et documenter un incident simulé.

---

## 3. Journal des Modifications

- **[Date] :**
    - **Action :** Initialisation du projet. Création de l'arborescence et des fichiers de suivi `PLAN_PROJET_RNCP.md` et `suivi_projet.md`.
    - **Décision :** Choix d'une architecture découplée FastAPI/Django pour bien séparer les responsabilités et couvrir les blocs de compétences.

---

## 4. Suivi des Erreurs

| Date | Erreur Rencontrée | Cause Analysée | Solution Apportée | Compétence Testée (ex: C21) |
|------|-------------------|----------------|-------------------|-----------------------------|
|      |                   |                |                   |                             |

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