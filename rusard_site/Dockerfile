# Utiliser une image Python officielle
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copier les fichiers de l'application
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer Django (en mode développement avec SQLite)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]