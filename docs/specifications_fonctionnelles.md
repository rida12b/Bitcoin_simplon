# Spécifications Fonctionnelles - Bitcoin Analyzer

**Projet :** Bitcoin Analyzer  
**Auteur :** Ridab  
**Version :** 1.0  
**Date :** [09/07/2025]

## 1. Contexte et Vision du Projet

Le marché des cryptomonnaies, et en particulier du Bitcoin, est caractérisé par une forte volatilité et un flux d'informations constant et dispersé. Pour un investisseur non-expert, il est difficile de se forger une opinion éclairée sans passer des heures à agréger et analyser des données de sources multiples.

**Vision :** "Bitcoin Analyzer" a pour but de devenir le tableau de bord de référence pour les investisseurs amateurs, en centralisant les données de marché, les actualités pertinentes et en fournissant une analyse de tendance simplifiée grâce à l'Intelligence Artificielle. L'objectif est de rendre l'information financière sur le Bitcoin **accessible, digeste et actionnable**.

## 2. Persona Utilisateur Cible

Pour guider la conception, nous définissons un persona utilisateur principal.

### **👤 Alex, 30 ans - L'Investisseur Prudent**

*   **Biographie :** Alex travaille dans le marketing et s'intéresse aux nouvelles technologies. Il a investi une petite partie de ses économies dans le Bitcoin mais n'a ni le temps ni l'expertise pour suivre les analyses financières complexes.
*   **Besoins et Objectifs :**
    *   Comprendre rapidement la "température" du marché chaque jour.
    *   Accéder aux nouvelles importantes qui pourraient influencer le cours.
    *   Visualiser la tendance récente sans avoir à lire des graphiques complexes.
*   **Frustrations actuelles :**
    *   "Je suis noyé sous le jargon technique sur Twitter et les sites spécialisés."
    *   "Je ne sais pas si une news est réellement importante ou si c'est juste du bruit."
    *   "Les graphiques de trading sont trop intimidants pour moi."

## 3. Récits Utilisateurs (User Stories)

Les fonctionnalités de l'application sont définies par les besoins de notre persona, Alex.

---

### **ID : US-01 - Consultation des Actualités Centralisées**

*   **En tant que** Alex, l'investisseur prudent,
*   **Je veux** consulter les titres des dernières actualités sur une seule et même page,
*   **Afin de** me tenir informé rapidement des événements majeurs sans avoir à visiter plusieurs sites.

**Critères d'Acceptation :**
*   Le tableau de bord doit afficher les 5 dernières actualités.
*   Chaque actualité doit afficher son titre complet.
*   Le titre de chaque actualité doit être un lien cliquable qui redirige vers l'article original dans un nouvel onglet.
*   Si aucune actualité n'est disponible, un message clair ("Aucune actualité à afficher.") doit apparaître.

---

### **ID : US-02 - Accès à une Analyse Simplifiée par l'IA**

*   **En tant que** Alex,
*   **Je veux** lire une analyse de la tendance du marché rédigée en langage simple et concis,
*   **Afin de** comprendre l'orientation générale du marché (haussière, baissière, stable) sans nécessiter de connaissances en analyse technique.

**Critères d'Acceptation :**
*   L'analyse doit être générée par le service d'Intelligence Artificielle.
*   Le texte de l'analyse ne doit pas dépasser 3 phrases pour rester concis.
*   L'analyse doit être présentée dans une section clairement identifiée ("Analyse de l'IA").
*   **Accessibilité :** Le fond de la section d'analyse doit avoir un contraste de couleur suffisant avec le texte pour être lisible (respect des normes WCAG AA).
*   En cas d'échec de la génération de l'analyse, la section ne doit pas s'afficher ou doit afficher un message d'erreur discret.

---

### **ID : US-03 - Visualisation de l'Historique Récent des Prix**

*   **En tant que** Alex,
*   **Je veux** voir un historique simple des prix de clôture des dernières 24 heures,
*   **Afin de** visualiser la volatilité récente du Bitcoin de manière factuelle.

**Critères d'Acceptation :**
*   Le tableau de bord doit afficher une liste ou un tableau des prix de clôture.
*   Chaque entrée doit indiquer le timestamp (ou l'heure) et le prix.
*   La liste doit être triée de la plus récente à la plus ancienne.
*   Par défaut, les 24 derniers points de données horaires sont affichés.

## 4. Fonctionnalités Hors Périmètre (Version 1.0)

Pour assurer une livraison rapide et ciblée, les fonctionnalités suivantes ne sont pas incluses dans la version initiale :

*   Création de comptes utilisateurs et authentification.
*   Personnalisation du tableau de bord.
*   Graphiques interactifs avancés.
*   Système d'alertes par email ou notification.