import os
import sys

# Ensure the Django project is importable when running tests locally.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "rusard_site"))

os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "testsecret"
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "rusard_site.settings",
)

import django
import pytest
from django.apps import apps
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.test.utils import (_TestState, setup_test_environment,
                               teardown_test_environment)

if not apps.ready:
    django.setup()


@pytest.fixture(scope="session", autouse=True)
def django_db_setup():
    """Initialise the Django test environment and database once per test run."""

    needs_teardown = False
    if not hasattr(_TestState, "saved_data"):
        setup_test_environment()
        needs_teardown = True
    call_command("migrate", run_syncdb=True, verbosity=0)
    yield
    if needs_teardown and hasattr(_TestState, "saved_data"):
        teardown_test_environment()


@pytest.fixture
def client():
    """Provide a Django test client without requiring pytest-django."""

    return Client()


@pytest.fixture
def django_user_model():
    """Expose the active user model for tests without pytest-django."""

    return get_user_model()


@pytest.fixture
def settings():
    """Expose Django settings and restore any modifications after each test."""

    preserved: dict[str, object] = {}
    for attribute in dir(django_settings):
        if attribute.isupper():
            preserved[attribute] = getattr(django_settings, attribute)

    yield django_settings

    current_attributes = {
        attribute for attribute in dir(django_settings) if attribute.isupper()
    }
    for attribute in current_attributes - set(preserved):
        delattr(django_settings, attribute)
    for attribute, value in preserved.items():
        setattr(django_settings, attribute, value)


@pytest.fixture(autouse=True)
def disable_secure_ssl_redirect(settings, monkeypatch):
    """Avoid HTTPS enforcement during tests so responses keep their status codes."""

    original = getattr(settings, "SECURE_SSL_REDIRECT", False)
    monkeypatch.setattr(settings, "SECURE_SSL_REDIRECT", False, raising=False)
    yield
    monkeypatch.setattr(settings, "SECURE_SSL_REDIRECT", original, raising=False)
