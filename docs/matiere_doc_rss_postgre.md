Document de Synthèse pour Rapport et Présentation : "Bitcoin Analyzer"
1. L'Histoire du Scraping : De l'Échec à la Robustesse (Compétence C21)
C'est un cas d'école parfait pour la compétence C21 (Résoudre les incidents techniques), car il démontre une capacité à diagnostiquer un problème et à choisir une solution stratégique plutôt qu'un simple correctif technique.
Comment le présenter :
Étape 1 : La Solution Initiale (qui fonctionnait).
Contexte : "Pour collecter les actualités, ma première approche a été de faire du web scraping sur news.bitcoin.com, un site dynamique nécessitant l'exécution de JavaScript."
Solution Technique : "J'ai donc utilisé la bibliothèque undetected-chromedriver pour piloter un vrai navigateur, attendre le chargement du contenu, et parser le HTML final. Cette solution a fonctionné et a permis de valider la faisabilité de la collecte." (Vous montrez ici votre capacité à gérer des sites complexes).
Étape 2 : L'Incident Technique.
Symptôme : "Après un certain temps, le script a commencé à échouer systématiquement. Les logs montraient des erreurs HTTP 403 ou des pages de vérification (captcha), indiquant que le site avait renforcé ses protections anti-bot."
Diagnostic : "L'analyse a confirmé que s'acharner sur cette cible devenait une course à l'armement technique. La solution était devenue fragile, peu fiable et difficile à maintenir en production."
Étape 3 : La Résolution Stratégique (le pivot vers RSS).
Décision : "Face à cet incident, la meilleure solution n'était pas une correction technique complexe, mais un pivot stratégique. J'ai décidé de changer de source pour une méthode plus fiable et conçue pour l'échange de données : les flux RSS."
Nouvelle Solution Technique : "J'ai réécrit le script extraction_news.py pour utiliser la bibliothèque feedparser et cibler le flux RSS de Google News. Cette approche est infiniment plus robuste car elle utilise un canal de communication standardisé, garantissant la pérennité et la fiabilité de la collecte de données."
Leçon Apprise : "Cet incident m'a appris qu'une bonne ingénierie, c'est aussi savoir abandonner une solution fragile au profit d'une approche plus stable pour garantir la continuité du service."
2. La Migration de la Base de Données : De SQLite à PostgreSQL (Préparation au Déploiement)
C'est une excellente démonstration des compétences liées à l'architecture (C15), au packaging (C19) et à la préparation à la mise en production.
Comment le présenter :
Étape 1 : Le Choix Initial pour le Développement (SQLite).
Contexte : "Pour la phase de développement et de prototypage rapide, j'ai choisi SQLite comme base de données."
Justification : "Ce choix était stratégique : SQLite est un simple fichier, ne nécessite aucun serveur, est intégré à Python et rend les tests locaux et l'intégration continue (CI) extrêmement simples et rapides. C'est le choix parfait pour démarrer."
Étape 2 : L'Analyse des Contraintes de Déploiement.
Problématique : "En préparant le déploiement de l'application sur un serveur cloud comme DigitalOcean, j'ai identifié une incompatibilité majeure. Ces environnements de production ont souvent un système de fichiers 'éphémère' : le fichier SQLite aurait été effacé à chaque redémarrage du service, entraînant une perte totale des données."
Diagnostic : "SQLite n'est donc pas une solution viable pour une application en production qui nécessite la persistance des données."
Étape 3 : La Migration vers une Solution Professionnelle (PostgreSQL).
Décision : "Pour garantir la robustesse, la persistance et la scalabilité de l'application, j'ai migré la couche de persistance vers PostgreSQL, le standard de l'industrie pour les applications web."
Mise en Œuvre Technique : "J'ai modifié l'API (api/app.py) pour utiliser la bibliothèque psycopg2 et se connecter via une variable d'environnement DATABASE_URL, ce qui est la pratique standard pour les déploiements professionnels."
Point Bonus (votre code le fait !) : "Pour conserver l'avantage de tests rapides et isolés, j'ai utilisé l'injection de dépendances de FastAPI. Ainsi, l'application utilise PostgreSQL en production, mais la suite de tests pytest continue d'utiliser une base de données SQLite temporaire, garantissant que nos tests restent rapides et ne dépendent pas d'un service externe."
3. Déploiement en Production : De la Théorie à la Pratique
Cette section documente le passage d'un environnement de développement à une architecture cloud distribuée et robuste, en détaillant les incidents rencontrés et leur résolution.
3.1 Architecture de Déploiement Cloud (C15)
Décision d'Architecture : "Pour le déploiement, j'ai opté pour une architecture distribuée : la base de données PostgreSQL est hébergée sur un service managé de Render pour la fiabilité et la simplicité de maintenance, tandis que les applications (API FastAPI et Frontend Django) tournent sur un VPS DigitalOcean pour la flexibilité et le contrôle."
3.2 Résolution d'Incidents de Déploiement (C21)
Incident 1 : L'API ne trouve pas les tables de la base de données.
Symptôme : L'API FastAPI démarrait, mais tous les endpoints retournaient une erreur 500. Les logs affichaient psycopg2.errors.UndefinedTable: relation "bitcoin_prices" does not exist.
Diagnostic : La connexion à la base de données Render fonctionnait (prouvé par un test avec psql), mais la base était vide. Les scripts de collecte de données (run_scripts.sh) étaient mal configurés et continuaient d'écrire dans une base de données SQLite locale sur le VPS, ignorant la base de données distante sur Render.
Résolution : J'ai refactorisé le module scripts/stockage.py pour qu'il détecte la présence de la variable d'environnement DATABASE_URL. S'il la trouve, il utilise psycopg2 pour se connecter à PostgreSQL ; sinon, il utilise sqlite3. Les scripts d'extraction ont été adaptés pour utiliser ces nouvelles fonctions. Après avoir relancé bash run_scripts.sh, les tables ont été correctement créées et peuplées sur la base Render.
Leçon Apprise : Il est crucial d'assurer la cohérence de la configuration de l'environnement sur toutes les parties d'une application, y compris les scripts de support et pas seulement l'API principale.
Incident 2 : Conflit de port sur le serveur.
Symptôme : En essayant de lancer l'API avec uvicorn, j'obtenais l'erreur address already in use sur le port 8001.
Diagnostic : La commande lsof -i :8001 a révélé que des processus gunicorn d'une précédente tentative de déploiement tournaient toujours en arrière-plan et occupaient le port.
Résolution : J'ai utilisé la commande pkill -f gunicorn pour arrêter proprement tous les processus Gunicorn existants, libérant ainsi le port.
Leçon Apprise : La gestion des processus est une compétence essentielle de l'administration système. Il faut toujours s'assurer qu'un port est libre avant de tenter de lancer un nouveau service.
3.3 Pérennisation des Services avec Systemd (C19 & MLOps)
Problématique : "Lancer les serveurs manuellement dans le terminal n'est pas une solution de production. Si le terminal est fermé ou si le serveur redémarre, l'application s'arrête."
Solution Professionnelle : "Pour transformer l'application en un service robuste, j'ai utilisé Systemd, le gestionnaire de services standard de Linux, pour piloter Gunicorn, un serveur de production."
Mise en Œuvre Technique :
Création d'un service pour l'API (gunicorn_api.service) : Un fichier de service a été créé dans /etc/systemd/system/ pour lancer l'API FastAPI avec Gunicorn, en spécifiant le chemin de l'environnement virtuel, le répertoire de travail et le nombre de workers.
Création d'un service pour le Frontend (gunicorn_django.service) : Un second fichier de service a été créé pour l'application Django. Une dépendance (After=gunicorn_api.service) a été ajoutée pour s'assurer que le backend est toujours démarré avant le frontend.
Gestion des Services : Les commandes sudo systemctl daemon-reload, sudo systemctl start [service], et sudo systemctl enable [service] ont été utilisées pour enregistrer, démarrer et activer les services au démarrage du serveur.
Résultat Final : "L'application est maintenant entièrement gérée par le système d'exploitation. Elle est lancée automatiquement, surveillée, et redémarrée en cas de problème, garantissant une haute disponibilité."