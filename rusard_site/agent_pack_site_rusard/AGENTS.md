# AGENTS.md — Agent ChatGPT Codecs pour *site-rusard*

Dernière génération : 2025-08-09 09:11

## 🎯 Objectif
Fournir à l’agent **ChatGPT Codecs** (Code Interpreter) tout le contexte et les règles pour travailler *en sécurité* sur le dépôt **site-rusard** (Django + Docker).

## 🧠 Ce que l’agent peut faire
- Lire/écrire des fichiers dans le repo (Python, YAML/ENV, Markdown, Docker).
- Générer ou modifier : vues, modèles, admin, tests, templates, configs.
- Lancer des commandes locales (sandbox) : linters, formatters, tests, scripts `scripts/*.sh`.
- Préparer un patch/commit (diff) et un journal d’exécution dans `logs/`.

## 🔒 Contraintes
- Pas d’accès Internet.
- Instructions claires et explicites.
- Toujours exécuter la séquence : format → lint → tests.
- Ne pas modifier de secrets.

## 🗂️ Structure
- `AGENTS.md` — règles de travail pour l’agent.
- `config.yaml` — paramètres (Python, commandes, chemins).
- `env/.env.example` — variables d’environnement d’exemple.
- `scripts/` — scripts standardisés pour formatage, lint, tests, migrations.
- `.github/workflows/ci.yml` — pipeline CI.

## ⚙️ config.yaml attendu
```yaml
python_version: "3.11"
project_name: "site-rusard"
django_settings_module: "rusard_site.settings"
manage_py: "manage.py"
run_sequence:
  - scripts/format.sh
  - scripts/lint.sh
  - scripts/test.sh
commit_message_template: "chore(agent): {title}"
exclude_paths:
  - node_modules/
  - logs/
  - .git/
```

## ✅ Procédure standard
1. Lire les fichiers à modifier.
2. Modifier le minimum nécessaire.
3. Exécuter : `scripts/format.sh` → `scripts/lint.sh` → `scripts/test.sh`.
4. Si modèle changé : `scripts/makemigrations.sh` puis `scripts/migrate.sh`.
5. Documenter le commit.
6. Écrire un log dans `logs/`.

## 🗣️ Prompts exemples
- Corrige un bug + ajoute test.
- Crée une nouvelle fonctionnalité Django + tests.
- Applique formatage et lint.

## 🧪 Tests
- Priorité aux tests unitaires rapides.
- Créer au moins un test si inexistant.

## 🔁 CI/CD
- `.github/workflows/ci.yml` relance format, lint, tests sur PR.
