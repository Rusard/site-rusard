from django.core import checks as django_checks

from rusard_site import checks


def test_required_settings_check_warns_when_using_placeholders(monkeypatch):
    for key in [
        "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD",
        "RECAPTCHA_PUBLIC_KEY",
        "RECAPTCHA_PRIVATE_KEY",
    ]:
        monkeypatch.delenv(key, raising=False)

    messages = checks.required_settings_check(None)

    assert not any(isinstance(message, django_checks.Critical) for message in messages)

    warning_ids = {
        message.id for message in messages if isinstance(message, django_checks.Warning)
    }

    assert {
        "rusard.E001.placeholder",
        "rusard.E002.placeholder",
        "rusard.E003.placeholder",
        "rusard.E004.placeholder",
        "rusard.E005.placeholder",
    }.issubset(warning_ids)
