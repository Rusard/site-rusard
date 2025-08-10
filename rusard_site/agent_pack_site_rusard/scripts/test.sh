#!/usr/bin/env bash
set -euo pipefail
if [ -f "manage.py" ]; then
  python manage.py check
  if [ -f "pytest.ini" ] || { [ -f "pyproject.toml" ] && grep -qi pytest pyproject.toml; }; then
    pytest -q || true
  else
    python manage.py test -v 2
  fi
else
  echo "manage.py not found"; exit 1
fi
