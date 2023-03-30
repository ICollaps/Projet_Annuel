# Projet annuel

## Contexte

Vous travaillez au sein de la MedTech Detect qui fournit des solutions d’IA permettant de détecter et dépister diverses pathologies à partir d’informations provenant d’un patient. L’entreprise est en train de déployer un nouveau produit permettant de prédire la Sepsis. Votre rôle, en tant que Machine Learning Engineer, est de mettre en place une nouvelle API qui sera le service backend de ce nouveau projet.

## Spécification

L’API devra disposer de 2 routes :

- `/health` : qui permet de déterminer l’état du système et renvoie ‘OK’ si tout va bien.
- `/predict/patient` : qui permet à partir des paramètres du patient de renvoyer si celui-ci est positif ‘Positive’ ou négatif ‘Negative’.

Pour toute incohérence détectée dans les données d’entrées, vous renverrez une erreur 422.

Une première étape du projet nécessaire à la réalisation de la route `/predict/patient` est de réaliser un modèle de machine learning permettant de prédire la variable cible. Cependant, pour la simple validation du projet, aucune précision particulière n’est demandée.

## Contraintes

Votre API doit s’intégrer dans l’écosystème tech déjà utilisé par l’entreprise. La majorité de ses services sont déployés sur AWS, notamment via des EC2. Le principal langage de leur codebase est Python.

## Pour aller plus loin..

Outre la mise en place d’un modèle simple permettant de prédire la variable target ainsi que de l’API, le projet peut s’enrichir de plusieurs étapes supplémentaires :

- Amélioration du modèle de prédiction
- Création d’une UI permettant d'interagir avec l’API

----------------------------

## Collecte et compréhension des données

- Obtenir des ensembles de données pertinents pour l'entraînement et la validation du modèle
- Nettoyer et prétraiter les données pour faciliter l'apprentissage du modèle

- Python 
- 2 jours

## Choix et dev Model de ML
- Python 
- 2 semaine
- SVM / RF / 

### Entrainer le model:
- 3/4 jours

### Validation :
- 1/2 jours

## Dev backend
- 2 semaines


## Dev front:
- HTML / CSS / JS
- 2 semaines


## Implémentation sur AWS
- EC2 (docker)
- 1 mois


# Plan de projet annuel

## Analyse des exigences et planification

- Planifier les ressources et le temps nécessaire pour chaque étape

## Collecte et préparation des données
### Technologie selectionnée: Python
### Durée du jour: - 2 jours
- Obtenir des ensembles de données pertinents pour l'entraînement et la validation du modèle
- Nettoyer et prétraiter les données pour faciliter l'apprentissage du modèle

## Création et entraînement du modèle de machine learning
### Technologie selectionnée: Python
### Durée du jour: - 2 Semaine
- Sélectionner un algorithme de machine learning approprié pour la prédiction de la sepsis
- Diviser les données en ensembles d'entraînement et de validation
- Entraîner le modèle sur l'ensemble d'entraînement
- Valider le modèle sur l'ensemble de validation

## Développement de l'API
### Technologie selectionnée: Python. Sklearn, Pandas, Numpy, Matplotlib
### Durée du jour: - 2 jours
- Mettre en place les deux routes requises (/health et /predict/patient) en utilisant un framework Python, comme Flask ou FastAPI
- Intégrer le modèle de machine learning entraîné à l'API
- Implémenter la gestion des erreurs et la validation des données d'entrée
- Tester l'API pour s'assurer qu'elle répond aux exigences

## Amélioration du modèle de prédiction (optionnel)
### Technologie selectionnée: Python. Sklearn, Pandas, Numpy, Matplotlib
### Durée du jour: - 4 jours
- Explorer différentes techniques d'optimisation et de sélection de caractéristiques pour améliorer les performances du modèle
- Mettre à jour le modèle dans l'API en conséquence

## Création d'une interface utilisateur (optionnel)
### Technologie selectionnée: HTML / CSS / JS
### Durée du jour: - 2 semaines
- Concevoir et développer une interface utilisateur simple pour interagir avec l'API
- Intégrer la communication avec l'API dans l'interface utilisateur
- Tester l'interface utilisateur pour s'assurer qu'elle fonctionne correctement avec l'API


## Déploiement de l'API sur AWS
### Technologie selectionnée: EC2 (docker)
### Durée du jour: - 1 mois
- Configurer une instance EC2 pour déployer l'API
- Installer et configurer les logiciels nécessaires sur l'instance EC2
- Déployer l'API sur l'instance EC2
- Configurer les paramètres de sécurité et les autorisations appropriées

## Documentation et maintenance

- Documenter le processus de développement, les choix techniques et les dépendances du projet
- Assurer la maintenance et les mises à jour régulières de l'API et du modèle de machine learning

## Bilan du projet

- Analyser les résultats et les performances du projet
- Recueillir les retours des utilisateurs et des parties prenantes
- Identifier les domaines d'amélioration pour les futures itérations du projet

# Scrum Planning

## 4 Sprints:

### 1er sprint
Sprint Goal: Obtenir un modele de machine learning entrainé et fonctionnel
Durée du sprint: 2 semaines
### 2eme sprint:
Sprint Goal: Implementation de l'application (back et front) sur un modele amélioré
Durée du sprint: 1 mois
### 3eme sprint: 
Sprint Goal: Déploiement du projet sur AWS
Durée du sprint: 3 semaines
### 4eme sprint: 
Sprint Goal: Amélioration de l'interface utilisateur et finalisation de la documentation
Durée du sprint: 1 Mois
