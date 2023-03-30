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
