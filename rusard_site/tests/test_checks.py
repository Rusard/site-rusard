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

    has_critical_messages = any(
        isinstance(message, django_checks.Critical) for message in messages
    )
    assert not has_critical_messages

    def is_warning(message):
        return isinstance(message, django_checks.Warning)

    warning_ids = {message.id for message in messages if is_warning(message)}

    assert {
        "rusard.E001.placeholder",
        "rusard.E002.placeholder",
        "rusard.E003.placeholder",
        "rusard.E004.placeholder",
        "rusard.E005.placeholder",
    }.issubset(warning_ids)
