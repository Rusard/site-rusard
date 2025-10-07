#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
REPO_ROOT="$(cd "${PROJECT_DIR}/.." && pwd)"

if [ ! -f "${PROJECT_DIR}/manage.py" ]; then
  echo "manage.py not found under ${PROJECT_DIR}" >&2
  exit 1
fi

pushd "${PROJECT_DIR}" >/dev/null

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-rusard_site.settings}"
export SECRET_KEY="${SECRET_KEY:-testsecret}"
export DATABASE_URL="${DATABASE_URL:-sqlite:///${PROJECT_DIR}/tests.sqlite3}"

# Ensure the project directory itself is importable.
case ":${PYTHONPATH:-}:" in
  *":${PROJECT_DIR}:"*) : ;; # already present
  *) export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}" ;;
esac

python manage.py check

popd >/dev/null

if [ -f "${REPO_ROOT}/pytest.ini" ] || { [ -f "${REPO_ROOT}/pyproject.toml" ] && grep -qi pytest "${REPO_ROOT}/pyproject.toml"; }; then
  pushd "${REPO_ROOT}" >/dev/null
  pytest -q
  popd >/dev/null
else
  pushd "${PROJECT_DIR}" >/dev/null
  python manage.py test -v 2
  popd >/dev/null
fi
