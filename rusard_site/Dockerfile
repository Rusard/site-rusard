# Utiliser une image Python officielle
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copier les fichiers de l'application
COPY . /app/

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh 
RUN chmod +x /usr/src/app/entrypoint.sh

# Exposer le port 8000
EXPOSE 8000

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Commande pour démarrer Django (en mode développement avec SQLite)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]