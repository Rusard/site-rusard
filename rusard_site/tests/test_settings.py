import pytest

from rusard_site import settings


@pytest.mark.parametrize(
    "env_key",
    ["SQL_USER", "SQL_PASSWORD", "SQL_HOST", "SQL_PORT", "SQL_DATABASE"],
)
def test_build_default_database_url_handles_missing_env(monkeypatch, env_key):
    monkeypatch.delenv(env_key, raising=False)

    url = settings.build_default_database_url()

    assert "None" not in url


def test_build_default_database_url_uses_expected_defaults(monkeypatch):
    for key in [
        "SQL_USER",
        "SQL_PASSWORD",
        "SQL_HOST",
        "SQL_PORT",
        "SQL_DATABASE",
    ]:
        monkeypatch.delenv(key, raising=False)

    expected_url = "postgres://postgres:postgres@localhost:5432/postgres"

    assert settings.build_default_database_url() == expected_url
