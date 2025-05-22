# 🌐 Rusard.ch — Site Web Personnel

Bienvenue sur le dépôt du site web [rusard.ch](https://rusard.ch) ! Ce projet est une application web construite avec Django, PostgreSQL, Docker, Nginx, Let's Encrypt, et déployée automatiquement via GitHub Actions.

## 🚀 Objectif

Développer un site vitrine professionnel avec des fonctionnalités comme :

* Pages statiques (Accueil, À propos, Contact, etc.)
* Formulaire de contact fonctionnel (via SMTP Infomaniak)
* Interface d’administration Django
* Intégration de Google Analytics
* Structure prête pour ajouter une partie dynamique (ex. blog, e-commerce)

## 🪰 Stack technique

* **Backend** : [Django](https://www.djangoproject.com/)
* **Base de données** : PostgreSQL
* **Serveur web** : Gunicorn + Nginx
* **Reverse Proxy** : nginx-proxy + acme-companion (Let's Encrypt)
* **Conteneurs** : Docker + Docker Compose
* **CI/CD** : GitHub Actions
* **Environnement Dev/Prod** : géré via `.env` + `Dockerfile` multi-stage

## 📦 Structure du dépôt

```
site-rusard/
├── rusard_site/             # Projet Django
│   └── settings.py          # Paramètres (configurables via .env)
├── rusardhome/              # App principale (templates, views, etc.)
├── nginx/                   # Config Nginx custom (SSL, redirection)
├── .env.prod                # Variables d'environnement pour la prod
├── docker-compose.prod.yml # Docker Compose pour la production
├── docker-compose.yml       # Docker Compose pour le développement
├── Dockerfile.prod          # Image multistage Django pour prod
└── .github/workflows/       # GitHub Actions (CI/CD)
```

## ⚙️ Développement local

1. Cloner le projet :

   ```bash
   git clone https://github.com/Rusard/site-rusard.git
   cd site-rusard
   ```

2. Créer un fichier `.env.dev` à partir de `.env.prod` avec tes variables de développement.

3. Lancer le projet :

   ```bash
   docker-compose up --build
   ```

4. Accéder au site sur [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🛠️ Déploiement automatique

Le site est déployé automatiquement sur le serveur VPS à chaque `push` sur la branche `master` grâce à un workflow GitHub Actions.

Le déploiement :

* Fait un `git pull` sur le serveur
* Reconstruit les conteneurs avec `docker-compose`
* Collecte les fichiers statiques
* Applique les éventuelles migrations

## 📩 Contact

Pour toute question ou suggestion :

* Email : [contact@rusard.ch](mailto:contact@rusard.ch)
* Contribuez en ouvrant une issue ou une pull request 🙌

---

### ✅ TODO (si vous voulez contribuer !)

* Blog
* e-commerce
* compte pour se connecter

---

Merci pour votre intérêt pour le projet 🙏
