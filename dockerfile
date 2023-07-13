# Utiliser une image de base Python 3.10
FROM python:3.10-slim-buster

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get -y upgrade

# Installer libgomp1 pour LightGBM
RUN apt-get install -y libgomp1

# Met à jour pip pour éviter des erreurs dans le futur
RUN pip install --upgrade pip

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers et les répertoires du répertoire actuel dans le chemin /app dans le conteneur
ADD . /app

# Installer les dépendances Python spécifiées dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 5000

# Définir la variable d'environnement pour indiquer où Flask doit s'exécuter
ENV FLASK_APP=app.py

# Définir la commande pour exécuter l'application Flask
CMD flask run --host=0.0.0.0