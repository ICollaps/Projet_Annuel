# Projet Annuel

Ce projet est une application web pour la prédiction de la sepsis à l'aide du machine learning. L'application a été développée en utilisant Python et Flask, et est conçue pour être déployée sur AWS EC2.

## Commencer

Ces instructions vous permettront d'obtenir une copie du projet en cours d'exécution sur votre machine locale à des fins de développement et de test.

### Prérequis

Le projet nécessite les outils et bibliothèques suivants :

- Python
- Flask
- PyMongo
- Flask-Login
- Werkzeug

## Installation

Pour obtenir une copie du projet et installer les prérequis nécessaires, suivez ces étapes :

1. Clonez le repo : `git clone <lien-du-repo>`
2. Naviguez jusqu'au répertoire du projet : `cd Projet_Annuel`
3. Installez les prérequis : Exécutez `pip install -r requirements.txt`

## Lancement de l'Application

Vous pouvez démarrer l'application en exécutant `python app.py` depuis le répertoire du projet. Cela démarrera le serveur de développement Flask sur votre machine locale. Vous pouvez visiter l'application en naviguant vers `http://localhost:5000` dans votre navigateur web.

## Routes de l'Application

L'application comprend plusieurs routes pour l'interaction de l'utilisateur :

### Routes de Connexion (`routes/login.py`)

- `/login`: Méthode POST pour la connexion de l'utilisateur.
- `/logout`: Route pour la déconnexion de l'utilisateur. Nécessite une connexion.
- `/register`: Méthodes GET et POST pour l'inscription de l'utilisateur.

### Routes du Patient (`routes/patient.py`)

- `/health`: Méthode GET. Nécessite une connexion. Utilisé pour rendre le formulaire d'entrée de l'utilisateur pour les données de santé.
- `/health/predict`: Méthode POST. Nécessite une connexion. Utilisé pour faire une prédiction basée sur les entrées de l'utilisateur.

### Routes Admin (`routes/admin.py`)

- `/delete`: Méthode GET. Nécessite une connexion. Utilisé pour supprimer un utilisateur.
- `/deletePatient`: Méthode GET. Nécessite une connexion. Utilisé pour supprimer un patient.
- `/deleteMedecin`: Méthode GET. Nécessite une connexion. Utilisé pour supprimer un médecin.

### Routes Medecin (`routes/medecin.py`)

- `/mes_patients`: Méthode GET. Nécessite une connexion. Utilisé pour rendre une liste de patients pour l'utilisateur actuel (médecin).
- `/mon_profil`: Méthode GET. Nécessite une connexion. Utilisé pour rendre le profil de l'utilisateur actuel (médecin).

## Exécution des Tests

Les tests pour ce projet sont situés dans le répertoire `tests`. Vous pouvez les exécuter à l'aide d'un exécuteur de tests comme pytest. Pour installer pytest, exécutez `pip install pytest`. Pour exécuter les tests, naviguez jusqu'au répertoire du projet et exécutez `pytest`.

## Déploiement

Le projet est conçu pour être déployé sur une instance AWS EC2. Vous devrez configurer une instance EC2 et la configurer pour exécuter des applications Python et Flask. Une fois que votre instance EC2 est configurée, vous pouvez déployer l'application en clonant le dépôt sur l'instance EC2, en installant les prérequis, et en démarrant le serveur Flask. Notez que pour un déploiement en production, vous devrez également configurer un serveur prêt pour la production comme Gunicorn ou uWSGI, et un serveur web comme Nginx pour agir comme un proxy inverse.

## Construit Avec

- [Python](https://www.python.org/): Le langage de programmation utilisé.
- [Flask](https://flask.palletsprojects.com/): Le framework web utilisé.
- [MongoDB](https://www.mongodb.com/): La base de données utilisée. Interface avec PyMongo dans l'application.

## Auteurs

- Novaretti Rémy
- Collas Pierre
- Delers Rémi

## Remerciements

- Quentin TOULOU pour l'aide apportée au projet lorsque nous avions des questions et des points bloquants.
- Marie-Caroline LONGIN pour l'enseignement de la méthodologie agile qui nous a beaucoup servi durant ce projet.