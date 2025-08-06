# Rapport de Projet de Certification

**Titre du Projet :** Bitcoin Analyzer  
**Candidat :** Rida Boualam 
**Certification Visée :** RNCP37827 - Développeur en Intelligence Artificielle  
**Date :** Juillet 2025

---

## Sommaire

1. **Introduction et Analyse du Besoin (C14)**

2. **Conception et Architecture Technique (C15)**

3. **Épreuve E1 : La Chaîne de la Donnée (Bloc 1, C1-C5)**

4. **Épreuves E2 & E3 : Intégration du Service d'IA (Bloc 2, C6-C13)**

5. **Épreuves E4 & E5 : L'Application Complète (Bloc 3, C14-C21)**

6. **Conclusion**

---

## 1. Introduction et Analyse du Besoin (Compétence C14)

### a. Contexte et Vision du Projet

Le marché des cryptomonnaies, et en particulier du Bitcoin, est caractérisé par une forte volatilité et un flux d'informations constant et dispersé. Pour un investisseur non-expert, il est difficile de se forger une opinion éclairée sans passer des heures à agréger et analyser des données de sources multiples.

**Vision :** "Bitcoin Analyzer" a pour but de devenir le tableau de bord de référence pour les investisseurs amateurs, en centralisant les données de marché, les actualités pertinentes et en fournissant une analyse de tendance simplifiée grâce à l'Intelligence Artificielle. L'objectif est de rendre l'information financière sur le Bitcoin **accessible, digeste et actionnable**.

### b. Persona Utilisateur Cible

Pour guider la conception, nous définissons un persona utilisateur principal.

#### **👤 Alex, 30 ans - L'Investisseur Prudent**

- **Biographie :** Alex travaille dans le marketing et s'intéresse aux nouvelles technologies. Il a investi une petite partie de ses économies dans le Bitcoin mais n'a ni le temps ni l'expertise pour suivre les analyses financières complexes.

- **Besoins et Objectifs :**
  
  - Comprendre rapidement la "température" du marché chaque jour.
  
  - Accéder aux nouvelles importantes qui pourraient influencer le cours.
  
  - Visualiser la tendance récente sans avoir à lire des graphiques complexes.

- **Frustrations actuelles :**
  
  - "Je suis noyé sous le jargon technique sur Twitter et les sites spécialisés."
  
  - "Je ne sais pas si une news est réellement importante ou si c'est juste du bruit."
  
  - "Les graphiques de trading sont trop intimidants pour moi."

### c. Récits Utilisateurs (User Stories)

Les fonctionnalités de l'application sont définies par les besoins de notre persona, Alex.

---

#### **ID : US-01 - Consultation des Actualités Centralisées**

- **En tant que** Alex, l'investisseur prudent,

- **Je veux** consulter les titres des dernières actualités sur une seule et même page,

- **Afin de** me tenir informé rapidement des événements majeurs sans avoir à visiter plusieurs sites.

**Critères d'Acceptation :**

- Le tableau de bord doit afficher les 5 dernières actualités.

- Chaque actualité doit afficher son titre complet.

- Le titre de chaque actualité doit être un lien cliquable qui redirige vers l'article original dans un nouvel onglet.

- Si aucune actualité n'est disponible, un message clair ("Aucune actualité à afficher.") doit apparaître.

---

#### **ID : US-02 - Accès à une Analyse Simplifiée par l'IA**

- **En tant que** Alex,

- **Je veux** lire une analyse de la tendance du marché rédigée en langage simple et concis,

- **Afin de** comprendre l'orientation générale du marché (haussière, baissière, stable) sans nécessiter de connaissances en analyse technique.

**Critères d'Acceptation :**

- L'analyse doit être générée par le service d'Intelligence Artificielle.

- Le texte de l'analyse ne doit pas dépasser 3 phrases pour rester concis.

- L'analyse doit être présentée dans une section clairement identifiée ("Analyse de l'IA").

- **Accessibilité :** Le fond de la section d'analyse doit avoir un contraste de couleur suffisant avec le texte pour être lisible (respect des normes WCAG AA).

- En cas d'échec de la génération de l'analyse, la section ne doit pas s'afficher ou doit afficher un message d'erreur discret.

---

#### **ID : US-03 - Visualisation de l'Historique Récent des Prix**

- **En tant que** Alex,

- **Je veux** voir un historique simple des prix de clôture des dernières 24 heures,

- **Afin de** visualiser la volatilité récente du Bitcoin de manière factuelle.

**Critères d'Acceptation :**

- Le tableau de bord doit afficher une liste ou un tableau des prix de clôture.

- Chaque entrée doit indiquer le timestamp (ou l'heure) et le prix.

- La liste doit être triée de la plus récente à la plus ancienne.

- Par défaut, les 24 derniers points de données horaires sont affichés.

### d. Fonctionnalités Hors Périmètre (Version 1.0)

Pour assurer une livraison rapide et ciblée, les fonctionnalités suivantes ne sont pas incluses dans la version initiale :

- Création de comptes utilisateurs et authentification.

- Personnalisation du tableau de bord.

- Graphiques interactifs avancés.

- Système d'alertes par email ou notification.

## 2. Conception et Architecture Technique (Compétence C15)

### a. Schéma d'Architecture Détaillé

![Untitled diagram _ Mermaid Chart-2025-07-09-121014.png](C:\Users\Ridab\Downloads\Untitled%20diagram%20_%20Mermaid%20Chart-2025-07-09-121014.png)

**Description des flux :**

1. L'utilisateur accède au tableau de bord via son navigateur, envoyant une requête au serveur **Django** sur le port 8000.

2. La vue Django agit comme un client et envoie des requêtes HTTP à l'API **FastAPI** sur le port 8001 pour obtenir les données (news, prix, analyse).

3. L'API FastAPI orchestre la récupération des données :  
   a. Elle interroge la base de données **SQLite** pour les données de marché et les actualités.  
   b. Elle appelle l'API externe de **Google Gemini** pour générer l'analyse de tendance.

4. FastAPI agrège les réponses et les retourne au format **JSON** à Django.

5. Django utilise ces données pour populer le template HTML et renvoie la page web complète au navigateur de l'utilisateur.

### b. Pile Technologique et Justification des Choix

Chaque technologie a été sélectionnée après une analyse de ses forces et de sa pertinence pour le projet, en considérant également des alternatives.

#### Langage : Python 3.11

- **Justification :** Choix naturel pour un projet d'IA grâce à son écosystème mature (Pandas, Scikit-learn pour des évolutions futures) et ses excellentes bibliothèques pour le développement web (fastapi, django) et l'accès aux données (requests, beautifulsoup4). Sa syntaxe claire favorise un développement rapide et une maintenance aisée.

#### Backend : FastAPI

- **Justification :**
  
  - **Haute Performance :** Basé sur Starlette et Pydantic, FastAPI est l'un des frameworks Python les plus rapides, idéal pour une API qui se doit d'être réactive.
  
  - **Documentation Automatique (validation de C5) :** Génère nativement une documentation interactive (Swagger UI / OpenAPI), ce qui est un gain de temps majeur et une exigence de qualité professionnelle pour toute API.
  
  - **Validation des Données :** Utilise Pydantic pour une validation robuste et claire des types de données en entrée et en sortie, réduisant ainsi les bugs.

- **Alternative Écartée :**
  
  - **Flask :** Bien que plus léger, Flask ne propose pas de validation de données ni de documentation automatique nativement. Les ajouter nécessiterait des bibliothèques tierces (ex: Flask-RESTful, Flasgger), complexifiant la maintenance et ajoutant des points de défaillance potentiels.
  
  - **Django REST Framework (DRF) :** Très puissant mais plus lourd et plus complexe à configurer pour une API simple comme celle-ci. L'approche "tout-en-un" de DRF était superflue, FastAPI offrant un meilleur équilibre performance/simplicité pour ce projet.

#### Frontend : Django

- **Justification :**
  
  - **Framework Complet ("Batteries included") :** Offre une structure robuste pour construire une application web complète avec un ORM, un système de templates puissant, et des fonctionnalités de sécurité intégrées.
  
  - **Démonstration de Compétence :** Utiliser Django comme simple consommateur d'API démontre la maîtrise des architectures découplées, une compétence très recherchée dans le monde professionnel, qui valorise la séparation des responsabilités.

- **Alternative Écartée :**
  
  - **Streamlit/Gradio :** Ces outils sont excellents pour des prototypes rapides de data science et des interfaces de démonstration de modèles. Cependant, ils offrent moins de contrôle sur le design (HTML/CSS) et la structure de l'application, les rendant moins adaptés pour construire une application web personnalisable et évolutive destinée à un utilisateur final.

#### Base de Données : SQLite

- **Justification :**
  
  - **Simplicité :** Aucune installation de serveur requise, la base de données est un simple fichier. C'est la solution parfaite pour le développement, les tests automatisés et un déploiement léger.
  
  - **Intégration Python :** Fait partie de la bibliothèque standard de Python, ne nécessitant aucune dépendance externe pour fonctionner.

- **Vision d'Évolution (Scalabilité) :** SQLite est suffisant pour la version 1 du projet. Pour une mise en production à plus grande échelle, l'architecture est pensée pour une migration future. Le code d'accès aux données étant bien isolé, il serait aisé de le remplacer par des appels à un SGBD plus robuste comme **PostgreSQL**. Cette anticipation démontre une réflexion sur le cycle de vie complet de l'application.

#### Service d'IA : Google Gemini Pro

- **Justification :** Le choix de ce modèle n'est pas arbitraire. Il est le résultat d'un benchmark formel documenté dans docs/benchmark_ia.md. Gemini Pro a été sélectionné car il offre le meilleur compromis entre :
  
  1. **Performance :** Un score Elo très compétitif sur la LMSys Chatbot Arena.
  
  2. **Coût :** Un tarif très abordable, rendant le projet économiquement viable.
  
  3. **Facilité d'intégration :** Une bibliothèque Python officielle (google-generativeai) claire et bien documentée.

## 3. Épreuve E1 : La Chaîne de la Donnée (Bloc 1, C1-C5)

Pour alimenter l'application, j'ai mis en place une chaîne de traitement de la donnée complète, fiable et automatisée. Cette chaîne couvre la collecte depuis des sources hétérogènes, le nettoyage, le stockage et la mise à disposition via une API REST, validant ainsi l'ensemble des compétences du Bloc 1.

### 3.1 Automatisation de l'Extraction Multi-sources (C1, C3)

La première étape a consisté à automatiser la collecte de données de natures différentes pour garantir une vision complète du marché.

#### Source 1 : API REST Externe (Coinalyze) - Compétence C1

Pour obtenir les données de marché financières (prix, volume), j'ai développé le script scripts/extraction_api.py. Il interroge l'API de Coinalyze de manière robuste et sécurisée. La sécurité des informations d'authentification a été une priorité : la clé API est stockée dans un fichier .env (exclu du contrôle de version via .gitignore) et chargée dynamiquement en mémoire grâce à la bibliothèque python-dotenv.



```
// Extrait de scripts/extraction_api.py
```

![Capture d’écran 2025-07-09 150407.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20150407.png)

#### Source 2 : Scraping Web (Bitcoin Magazine) - Compétence C1

Pour les actualités, qui n'étaient pas disponibles via une API simple, j'ai développé le script scripts/extraction_news.py. Il utilise les bibliothèques requests pour télécharger le contenu HTML de la page d'actualités et BeautifulSoup pour le parser. Un User-Agent spécifique est défini dans les en-têtes pour simuler un navigateur légitime et éviter les blocages de sécurité courants. Ce processus transforme efficacement des données non structurées (HTML) en données structurées (une liste d'articles avec titre et lien).



// Extrait de scripts/extraction_news.py - Compétence C1



![](C:\Users\Ridab\AppData\Roaming\marktext\images\2025-07-09-15-44-22-image.png)

![](C:\Users\Ridab\AppData\Roaming\marktext\images\2025-07-09-15-44-52-image.png)





#### Agrégation et Nettoyage - Compétence C3

Une fois les données brutes extraites, elles sont immédiatement nettoyées et formatées pour garantir leur qualité et leur homogénéité avant le stockage. Par exemple, dans extraction_api.py, les données JSON de l'API sont transformées en une liste de dictionnaires Python avec des clés normalisées (timestamp, open, high, low, close, volume), préparant ainsi le jeu de données final.

### 3.2 Extraction via Requêtes SQL (C2)

Pour démontrer la capacité à interagir avec des systèmes d'information existants (un cas très courant en entreprise), j'ai simulé une base de données "legacy" et développé un script pour en extraire les données via des requêtes SQL standard.

D'abord, le script scripts/setup_source_db.py crée une base de données source_data.db contenant une table legacy_articles.  
Ensuite, le script scripts/extraction_sql.py se connecte à cette base source et exécute une requête SQL SELECT pour récupérer les articles.

```
// Extrait de scripts/extraction_sql.py - Compétence C2
```

![Capture d’écran 2025-07-09 150143.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20150143.png)

Les données sont ensuite traitées et insérées dans la base principale

Cette approche valide la maîtrise de l'extraction de données depuis un SGBD via le langage SQL.

### 3.3 Stockage et Modélisation des Données (C4)

Toutes les données collectées et nettoyées sont centralisées dans une base de données SQLite unique, data/bitcoin.db. Le module scripts/stockage.py est responsable de la création de la base et de la définition du schéma des tables.

Pour garantir l'intégrité des données et l'idempotence des scripts de collecte (c'est-à-dire qu'on peut les lancer plusieurs fois sans créer de doublons), des contraintes UNIQUE ont été placées sur les champs clés.

```
// Schéma SQL défini dans scripts/stockage.py - Compétence C4
-- Création de la table pour les prix du Bitcoin
```

![Capture d’écran 2025-07-09 150013.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20150013.png)

Cette modélisation rigoureuse assure la fiabilité et la cohérence du jeu de données qui alimentera l'application.

### 3.4 Exposition des Données via une API REST (C5)

La dernière étape du Bloc 1 consiste à rendre les données stockées accessibles de manière programmatique. J'ai développé pour cela une API en utilisant le framework FastAPI, choisi pour sa performance et sa capacité à générer automatiquement une documentation conforme au standard OpenAPI.

L'API, définie dans api/app.py, expose plusieurs endpoints, dont :

- /latest-news : pour récupérer les dernières actualités.

- /price-history : pour obtenir l'historique des prix.

L'un des livrables les plus importants de cette compétence est la documentation interactive (Swagger UI) générée automatiquement par FastAPI. Elle permet à n'importe quel développeur (ou au jury) de comprendre et de tester l'API sans avoir à lire une ligne de code, ce qui est une pratique professionnelle essentielle.

> **Figure 1 : Documentation interactive de l'API (Swagger UI) générée automatiquement par FastAPI.** On peut y voir les endpoints disponibles (`/latest-price`, `/price-history`), leurs paramètres, ainsi que la possibilité de les tester en direct, validant la compétence C5.
> 
> ![Capture d’écran 2025-07-09 142143.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20142143.png)

![Capture d’écran 2025-07-09 142231.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20142231.png)

![Capture d’écran 2025-07-09 142253.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20142253.png)

## 4. Épreuves E2 & E3 : Intégration du Service d'IA (Bloc 2, C6-C13)

Une fois la chaîne de données établie, le cœur du projet a été d'enrichir ces données grâce à un service d'intelligence artificielle. Ce bloc démontre une approche professionnelle complète : de la veille technologique à la sélection du modèle, son intégration, son exposition via une API, et enfin, la mise en place de tests et d'une chaîne de livraison continue pour garantir sa fiabilité.

### 4.1 Veille, Benchmark et Sélection du Service (E2 : C6, C7, C8)

Le choix d'un service d'IA ne doit pas être arbitraire. Il doit résulter d'une analyse rigoureuse de l'état de l'art et des contraintes du projet.

#### 4.1.1 Veille Technologique Active (C6)

Pour garantir que le projet utilise des technologies pertinentes et des pratiques à jour, une veille technologique active a été menée. Plutôt qu'une simple lecture passive, la méthodologie s'est concentrée sur des sources primaires et des discussions techniques :

- **Suivi de Dépôts GitHub Clés :** Surveillance active des issues, discussions et releases de projets comme google/generative-ai-python et tiangolo/fastapi.

- **Consultation de Listes "Awesome" :** Suivi régulier de listes communautaires comme awesome-generative-ai pour découvrir de nouveaux outils.

- **Analyse de Plateformes Techniques :** Participation aux discussions sur Twitter et Reddit (r/Cursor).

Cette veille, documentée dans docs/veille_technologique.md, a permis d'identifier des opportunités concrètes. Par exemple, la découverte de la bibliothèque litellm a été notée comme une piste d'évolution intéressante pour une future V2 du projet afin de supporter plusieurs modèles d'IA de manière unifiée.

#### 4.1.2 Benchmark et Sélection du Modèle d'IA (C7)

Le choix du modèle de langage (LLM) est une décision technique critique qui impacte directement la performance, le coût et la viabilité du projet. Pour garantir une décision objective et professionnelle, j'ai réalisé un benchmark formel, détaillé dans le document docs/benchmark_ia.md.

**Méthodologie de Benchmark :**  
La sélection s'est basée sur les données du leaderboard **Artificial Analysis AI**, une source spécialisée dans l'évaluation des fournisseurs d'API pour les développeurs. Cette source a été privilégiée pour son focus sur des métriques concrètes et directement applicables à notre projet :

1. **Qualité d'Analyse  :** Basée sur l'**"Artificial Analysis Intelligence Index"**, un score propriétaire qui évalue la capacité de raisonnement du modèle. C'est le critère le plus important.

2. **Coût de l'API  :** Basé sur le **"Blended USD/1M Tokens"**, un prix mixte qui reflète un usage réaliste. Crucial pour la viabilité économique.

3. **Vitesse de Réponse  :** Mesurée par le **"Total Response (s)"** en secondes. Un facteur important pour l'expérience utilisateur, bien que non-critique pour notre cas d'usage asynchrone.

**Alternatives Étudiées :**  
J'ai comparé plusieurs des modèles les plus performants et pertinents du marché :

- **Google Gemini 2.5 Pro (AI Studio)** : Le candidat principal.

- **OpenAI o3 (via OpenAI et Azure)** : Le concurrent direct en termes de qualité.

- **OpenAI o4-mini (via OpenAI et Azure)** : Un challenger très compétitif sur le plan du coût.

- **DeepSeek R1 0528** : Une alternative open-source très performante et économique.

**Tableau Comparatif Synthétique (basé sur Artificial Analysis AI) :**

![](C:\Users\Ridab\AppData\Roaming\marktext\images\2025-07-09-14-42-34-image.png)



**Décision Finale et Justification Technique :**

Le choix s'est porté sur **Google Gemini 2.5 Pro**. Cette décision est justifiée par une combinaison de performance de pointe et de flexibilité stratégique :

- **Performance de Pointe (Critère n°1) :** Gemini 2.5 Pro atteint le score d'intelligence maximal de **70** sur le benchmark Artificial Analysis, le plaçant au sommet du marché en termes de capacité de raisonnement. C'était le critère non négociable pour garantir la qualité des analyses fournies à l'utilisateur.

- **Avantage Stratégique - Fenêtre de Contexte :** Avec une fenêtre de contexte de **1 million de tokens**, ce modèle offre des perspectives d'évolution majeures pour l'analyse de documents financiers longs ou de multiples sources d'actualités, une capacité que peu de concurrents égalent.

- **Flexibilité Architecturale et Économique :** L'écosystème Gemini permet de basculer de manière transparente vers un modèle plus rapide et économique comme **Gemini 2.5 Flash** via une simple modification du nom du modèle dans l'appel API. Cette agilité permet d'optimiser les coûts ou la latence à l'avenir **sans aucune refonte de l'architecture**, ce qui représente un atout majeur en termes de maintenabilité et de coût à long terme.

En somme, Gemini 2.5 Pro a été choisi non seulement pour sa performance brute actuelle, mais aussi pour sa **flexibilité et son potentiel d'évolution**, garantissant la pérennité et l'agilité technique du projet.

#### 4.1.3 Paramétrage du Service (C8)

L'intégration du service Gemini Pro a été réalisée via la bibliothèque Python officielle google-generativeai. Conformément aux bonnes pratiques de sécurité, la clé d'API a été configurée via une variable d'environnement, chargée par python-dotenv, garantissant qu'aucune information sensible n'est exposée dans le code source.

### 4.2 Exposition et Intégration du Modèle (E3 : C9, C10)

#### 4.2.1 Exposition du Modèle via l'API (C9)

La valeur ajoutée de l'IA est exposée via l'endpoint /price-analysis de l'API FastAPI. Cet endpoint ne se contente pas de relayer une requête ; il met en œuvre une stratégie de prompt engineering pour maximiser la pertinence de la réponse du LLM.

Le processus est le suivant :

1. Récupérer l'historique récent des prix depuis la base de données SQLite.

2. Formatter ces données numériques en un texte descriptif et compréhensible.

3. Construire un prompt détaillé qui assigne un rôle au modèle ("Tu es un analyste financier pour un débutant"), fournit le contexte (les données de prix) et spécifie le format de la réponse attendue (concise et en langage simple).

4. Appeler le module d'analyse IA avec ce prompt.

5. Retourner la réponse textuelle du modèle dans un format JSON propre.

```
// Extrait de api/app.py - Compétence C9
```

![Capture d’écran 2025-07-09 145722.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20145722.png)

#### 4.2.2 Intégration dans l'Application Frontend (C10)

Cette fonctionnalité d'IA est ensuite rendue accessible à l'utilisateur final. L'application Django, agissant comme un client, envoie une requête HTTP à l'endpoint /price-analysis de l'API FastAPI pour récupérer l'analyse et l'afficher sur le tableau de bord. Cette communication inter-services est une démonstration clé de l'architecture découplée du projet.

### 4.3 Monitoring, Tests et CI/CD du Service IA (E3 : C11, C12, C13)

Pour assurer la qualité et la robustesse du service d'IA, une approche MLOps a été adoptée, intégrant le monitoring, les tests automatisés et la livraison continue.

#### 4.3.1 Monitoring du Modèle (C11)

Le module logging de Python a été intégré dans l'API FastAPI pour tracer de manière exhaustive toutes les interactions avec le service d'IA. Chaque appel à l'endpoint /price-analysis génère des logs qui permettent de suivre :

- La réception de la requête.

- Le début de l'appel à l'API externe de Gemini.

- La réception réussie de la réponse.

- Toute erreur survenant durant le processus.

**Preuve de logging (Extrait de docs/exemples_de_logs.txt) :**

```
2025-07-09 10:23:39,098 - INFO - API - Requête reçue pour l'analyse de prix (limite=24).2025-07-09 10:23:39,103 - INFO - API - Appel au service d'analyse IA (Gemini)...
2025-07-09 10:23:46,068 - INFO - API - Analyse IA reçue avec succès.
INFO:     127.0.0.1:61446 - "GET /price-analysis HTTP/1.1" 200 OK
```

Ce monitoring est essentiel pour le diagnostic d'incidents et le suivi de la performance en production.

#### 4.3.2 Tests Automatisés du Modèle (C12)

Tester un composant qui dépend d'une API externe payante pose un défi. La solution est de l'isoler en utilisant la technique du mocking. Le script tests/test_llm_analyzer.py utilise le décorateur @patch de la bibliothèque unittest.mock pour remplacer l'appel réel à l'API Gemini par une réponse simulée et contrôlée.

Cette approche permet de :

- Valider la logique interne de notre fonction analyze_text (construction du prompt, traitement de la réponse).

- Exécuter les tests rapidement et sans dépendance réseau.

- Éviter tout coût lié aux appels d'API pendant les tests.

- Garantir la reproductibilité des tests.

```
// Extrait de tests/test_llm_analyzer.py - Compétence C12
```

![](C:\Users\Ridab\AppData\Roaming\marktext\images\2025-07-09-15-07-21-image.png)

#### 4.3.3 Chaîne de Livraison Continue (C13)

Pour automatiser le processus de validation, une chaîne d'intégration continue a été mise en place avec GitHub Actions. Le fichier de configuration .github/workflows/ci.yml définit un workflow qui se déclenche à chaque modification du code.

**Étapes du workflow :**

1. **Checkout :** Récupération de la dernière version du code.

2. **Setup Python :** Installation de l'environnement Python.

3. **Install Dependencies :** Installation de toutes les bibliothèques listées dans requirements.txt.

4. **Prepare Test Database :** Exécution du script tests/setup_test_db.py pour créer une base de données de test propre.

5. **Run Tests :** Lancement de la suite de tests pytest.

Si l'une de ces étapes échoue, le workflow est marqué comme "échoué", empêchant l'intégration de code défectueux.

![Capture d’écran 2025-07-09 101207.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20101207.png)

![Capture d’écran 2025-07-09 101324.png](C:\Users\Ridab\Pictures\Screenshots\capture%20projet%20simplon\Capture%20d’écran%202025-07-09%20101324.png)

## 5. Épreuves E4 & E5 : L'Application Complète (Bloc 3, C14-C21)

Pour rendre le service d'analyse accessible à l'utilisateur final "Alex", j'ai développé une application web complète avec Django. Cette application ne contient pas de logique métier complexe ; son rôle est d'agir en tant que client de l'API FastAPI. Cette approche met en œuvre une architecture microservices découplée, une pratique standard dans l'industrie. Le cycle de vie de cette application est géré par des tests, une chaîne de livraison continue et une surveillance active, validant ainsi les compétences du Bloc 3.

### 5.1 Développement de l'Application Frontend (E4 : C16, C17)

#### 5.1.1 Conception de l'Application Django (C16)

La structure du projet respecte les conventions de Django pour garantir la clarté et la maintenabilité :

- Un projet principal dashboard gère la configuration globale.

- Une application viewer contient toute la logique de présentation.

- Le routage est géré de manière hiérarchique : dashboard/urls.py délègue les requêtes à viewer/urls.py grâce à la fonction include(), ce qui permet une organisation modulaire du code.

#### 5.1.2 Vue Principale et Logique de Consommation d'API (C17)

La vue viewer/views.py est le cœur de l'application frontend. Elle est responsable d'appeler les différents endpoints de l'API FastAPI, de collecter les données, et de les transmettre au template pour l'affichage. Une attention particulière a été portée à la robustesse : un bloc try...except global gère les erreurs de communication avec l'API, garantissant que l'application ne plante pas si le backend est indisponible.

```
// Extrait de viewer/views.py - Compétences C10, C17
from django.shortcuts import render
import requests
import logging

logger = logging.getLogger(__name__)
API_BASE_URL = "http://127.0.0.1:8001"

def news_list(request):
    """    Récupère toutes les données de l'API FastAPI pour les afficher sur un tableau de bord.    """
    logger.info(f"Requête reçue pour le tableau de bord depuis l'IP : {request.META.get('REMOTE_ADDR')}")
    context = {
        'news_list': [],
        'price_history': [],
        'price_analysis': "Analyse non disponible.",
        'error_message': None
    }

    try:
        # Appels successifs aux endpoints de l'API backend
        news_response = requests.get(f"{API_BASE_URL}/latest-news?limit=5", timeout=5)
        news_response.raise_for_status()
        context['news_list'] = news_response.json()

        history_response = requests.get(f"{API_BASE_URL}/price-history?limit=24", timeout=5)
        history_response.raise_for_status()
        context['price_history'] = history_response.json()

        analysis_response = requests.get(f"{API_BASE_URL}/price-analysis", timeout=15)
        analysis_response.raise_for_status()
        context['price_analysis'] = analysis_response.json().get('analysis', "Format d'analyse inattendu.")

    except requests.exceptions.RequestException as e:
        # Gestion centralisée des erreurs de communication avec le backend
        error_message = f"Erreur de communication avec l'API backend : {e}"
        logger.error(error_message, exc_info=True)
        context['error_message'] = "Le service d'analyse est actuellement indisponible. Veuillez réessayer plus tard."

    return render(request, 'viewer/news_list.html', context)
```

#### 5.1.3 Interface Utilisateur avec les Templates Django (C17)


Le template viewer/templates/viewer/news_list.html utilise non seulement le langage de template de Django pour afficher les données de manière dynamique, mais intègre également un design CSS moderne pour améliorer significativement l'expérience utilisateur (UX).

- **Structure et Design :** L'interface est structurée en "cartes" (cards) disposées sur une grille, ce qui permet de segmenter clairement l'information (Analyse IA, Actualités, Historique des Prix). L'utilisation d'icônes (via Font Awesome) et d'une typographie soignée renforce la lisibilité.
- **Logique d'Affichage :** Le template intègre des structures de contrôle avancées comme `{% for ... %}` avec `{% empty %}` pour gérer élégamment les cas où aucune donnée n'est disponible, et `{% if error_message %}` pour afficher des messages d'erreur clairs et stylisés à l'utilisateur.
- **Formatage des Données :** Pour améliorer l'accessibilité de l'information, les données brutes comme les timestamps Unix sont pré-traitées dans la vue Django avant d'être envoyées au template. Elles sont ainsi affichées sous une forme lisible et compréhensible par l'utilisateur (ex: `09 Jul 2025, 10:21`).
  Ce travail démontre la capacité à créer une interface non seulement fonctionnelle mais aussi esthétique et intuitive, en respectant les standards du web moderne.

```
//Interface Utilisateur Django
```

![](C:\Users\Ridab\AppData\Roaming\marktext\images\2025-07-09-16-04-59-image.png)

### 5.2 Tests, Packaging et Livraison Continue (E4 : C18, C19)

#### 5.2.1 Automatisation des Tests d'API (C18)

Pour garantir que l'API FastAPI fonctionne comme prévu, des tests d'intégration ont été écrits dans tests/test_api.py. Ces tests utilisent le TestClient de FastAPI pour simuler des requêtes HTTP vers les endpoints et valider leurs réponses. Crucialement, ces tests s'exécutent contre une base de données de test dédiée et isolée (créée par tests/setup_test_db.py), ce qui garantit des résultats fiables et reproductibles sans affecter les données de développement.

```
// Extrait de tests/test_api.py - Compétence C18
from fastapi.testclient import TestClient
from api.app import app
import os

# Forcer l'API à utiliser la base de données de test
import api.app
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_database.db')
api.app.DB_PATH = TEST_DB_PATH

client = TestClient(app)

def test_get_latest_news():
    """Teste si l'API retourne bien la nouvelle de test."""
    response = client.get("/latest-news")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['title'] == "Titre de test"
```

#### 5.2.2 Packaging avec Docker pour la Livraison Continue (C19)

Pour finaliser le processus de livraison, l'API FastAPI a été packagée dans une image Docker. Le dockerfile est optimisé pour la production :

- Il utilise une image de base légère (python:3.11-slim).

- Il sépare la copie et l'installation des dépendances du reste du code pour tirer parti du cache Docker.

- Il expose le port de l'application et définit la commande de démarrage du serveur.

```
# Extrait du dockerfile - Compétence C19

# Étape 1: Partir d'une image Python officielle et légère
FROM python:3.11-slim

# Étape 2: Définir le répertoire de travail
WORKDIR /app

# Étape 3: Copier uniquement le fichier des dépendances pour optimiser le cache
COPY requirements.txt .

# Étape 4: Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier tout le reste du code
COPY . .

# Étape 6: Exposer le port que l'API utilisera
EXPOSE 8001

# Étape 7: La commande à exécuter au démarrage
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"]
```

Ce conteneur est un artefact standard, portable et prêt à être déployé sur n'importe quel environnement, complétant ainsi la chaîne de livraison continue.

### 5.3 Surveillance et Résolution d'Incidents (E5 : C20, C21)

#### 5.3.1 Surveillance de l'Application (C20)

En plus du monitoring du backend, une journalisation a été implémentée dans l'application frontend Django. La vue principale logue les requêtes entrantes des utilisateurs ainsi que les appels sortants vers l'API FastAPI. Cela permet d'avoir une traçabilité complète du parcours d'une requête, de l'utilisateur final jusqu'au service d'IA, ce qui est indispensable pour le diagnostic en production.

**Preuve de logging (Extrait de docs/exemples_de_logs.txt) :**

```
// Logs générés par Django lors d'une requête utilisateur
Requête reçue pour le tableau de bord depuis l'IP : 127.0.0.1
Début de l'appel API vers : http://127.0.0.1:8001/latest-news?limit=5
Succès : 3 actualités récupérées.
Début de l'appel API vers : http://127.0.0.1:8001/price-history?limit=24
Succès : 24 points d'historique récupérés.
Début de l'appel API vers : http://127.0.0.1:8001/price-analysis
Succès : Analyse de l'IA récupérée.
```



#### 5.3.2 Résolution d'Incidents Techniques (C21)

Le développement d'une architecture multi-services a présenté des défis concrets. La capacité à diagnostiquer et résoudre ces incidents est une compétence fondamentale. Deux exemples significatifs sont documentés ci-dessous.

**Incident 1 : Conflit de Port entre Services**

- **Contexte :** Lors du premier lancement simultané de Django et FastAPI, l'application frontend ne parvenait pas à contacter le backend.

- **Symptôme :** Les logs de Django affichaient une requests.exceptions.ConnectionError.

- **Diagnostic :** Une analyse rapide a montré que les deux serveurs tentaient d'utiliser le port 8000 par défaut, créant une collision qui empêchait l'un des deux de démarrer correctement.

- **Résolution :** Le serveur FastAPI a été explicitement lancé sur le port 8001 via la commande uvicorn api.app:app --port 8001. L'URL de base dans la vue Django a été mise à jour en conséquence.

- **Leçon Apprise :** Cet incident m'a appris l'importance de la configuration explicite et de la documentation de la topologie réseau, même dans un projet local, pour éviter les conflits dans une architecture microservices.

**Incident 2 : Erreur d'Environnement dans la CI/CD**

- **Contexte :** Le premier workflow GitHub Actions échouait systématiquement, alors que tous les tests passaient en local.

- **Symptôme :** Les logs du runner GitHub affichaient une erreur ModuleNotFoundError: No module named 'httpx'.

- **Diagnostic :** L'erreur indiquait que l'environnement de la CI ne disposait pas de toutes les dépendances nécessaires. Le paquet httpx (une dépendance de fastapi.testclient) avait été installé manuellement en local mais n'avait pas été ajouté au fichier requirements.txt.

- **Résolution :** La dépendance manquante a été ajoutée au fichier requirements.txt. Après un nouveau commit, le workflow s'est exécuté avec succès.

- **Leçon Apprise :** Cet incident a été une démonstration pratique de la valeur de l'intégration continue. Elle force la discipline dans la gestion des dépendances et garantit la reproductibilité des environnements, évitant ainsi le classique "ça marche sur ma machine".

## 6. Conclusion

Ce projet, "Bitcoin Analyzer", a permis de construire de bout en bout une application full-stack et pilotée par l'IA, en respectant les standards professionnels de développement logiciel. Allant bien au-delà d'un simple prototype, le résultat est un service robuste, testé, documenté et prêt à être déployé, qui valide l'ensemble des compétences requises par le titre de Développeur en Intelligence Artificielle.

### 6.1 Bilan du Projet et Couverture des Compétences

L'objectif initial, qui était de fournir une information financière centralisée et analysée, a été pleinement atteint. L'architecture découplée, séparant le backend FastAPI du frontend Django, a prouvé sa pertinence en permettant un développement modulaire et une gestion claire des responsabilités. L'intégration d'un service d'IA (Google Gemini), sélectionné après une analyse rigoureuse, a permis d'ajouter une valeur métier significative aux données brutes.

Le projet couvre de manière exhaustive les compétences du référentiel RNCP37827 :

| Bloc de Compétences                 | Compétences Validées | Preuves Concrètes dans le Projet                                                                                                                             |
| ----------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Bloc 1 : La Chaîne de la Donnée** | C1-C5                | Scripts de collecte multi-sources (api, web, sql), modélisation de la BDD, et exposition via une API REST documentée (Swagger UI).                           |
| **Bloc 2 : Intégration de l'IA**    | C6-C13               | Documents de veille et de benchmark, intégration de Gemini, tests unitaires avec "mocking", et pipeline de CI/CD avec GitHub Actions.                        |
| **Bloc 3 : Application & MLOps**    | C14-C21              | Conception de l'application Django, consommation de l'API, packaging avec Docker, surveillance via logging, et résolution documentée d'incidents techniques. |

L'approche adoptée, axée sur les tests automatisés, l'intégration continue et la résolution méthodique d'incidents, démontre une maîtrise des pratiques MLOps et DevOps essentielles pour garantir la qualité et la maintenabilité d'un produit d'IA en conditions réelles.

### 6.2 Perspectives d'Évolution

Le projet a été conçu pour être une fondation solide. Plusieurs axes d'évolution sont envisagés pour l'avenir, démontrant une vision à long terme du cycle de vie de l'application :

- **Montée en charge et Performance :**
  
  - **Base de Données :** Migration de SQLite vers un SGBD plus robuste comme PostgreSQL pour gérer un plus grand volume de données et des requêtes plus complexes.
  
  - **Caching :** Implémentation d'un système de cache avec Redis pour les endpoints les plus sollicités de l'API afin de réduire la latence et le nombre d'appels à la base de données.

- **Sécurité et Fiabilité :**
  
  - **Authentification :** Sécurisation de l'API avec un système d'authentification comme OAuth2 pour contrôler l'accès aux endpoints.
  
  - **Déploiement Professionnel :** Déploiement de l'image Docker de l'API sur un service de conteneurisation cloud (ex: AWS Fargate, Google Cloud Run) et déploiement de l'application Django, le tout intégré au pipeline de CI/CD pour un déploiement continu.

- **Fonctionnalités Métier :**
  
  - **Analyse Avancée :** Entraînement ou fine-tuning d'un modèle de langage spécialisé sur des données financières pour fournir des analyses encore plus précises et prédictives.
  
  - **Interactivité :** Ajout de graphiques interactifs sur le frontend pour une meilleure visualisation des données de marché.

Ce projet ne marque pas une fin, mais le début d'un produit potentiellement viable, dont l'architecture a été pensée dès le départ pour supporter ces évolutions futures.
