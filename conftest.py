import os
import sys

# Ensure the Django project is importable when running tests locally.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "rusard_site"))

os.environ.setdefault("SECRET_KEY", "testsecret")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "rusard_site.rusard_site.settings",
)

