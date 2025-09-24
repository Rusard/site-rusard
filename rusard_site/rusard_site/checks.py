from django.conf import settings
from django.core import checks

REQUIRED_CONFIGURATION = (
    (
        "EMAIL_HOST_USER",
        settings.EMAIL_HOST_USER,
        "rusard.E001",
        "EMAIL_HOST_USER doit être défini dans l'environnement.",
    ),
    (
        "EMAIL_HOST_PASSWORD",
        settings.EMAIL_HOST_PASSWORD,
        "rusard.E002",
        "EMAIL_HOST_PASSWORD doit être défini dans l'environnement.",
    ),
    (
        "RECAPTCHA_PUBLIC_KEY",
        settings.RECAPTCHA_PUBLIC_KEY,
        "rusard.E003",
        "RECAPTCHA_PUBLIC_KEY doit être défini dans l'environnement.",
    ),
    (
        "RECAPTCHA_PRIVATE_KEY",
        settings.RECAPTCHA_PRIVATE_KEY,
        "rusard.E004",
        "RECAPTCHA_PRIVATE_KEY doit être défini dans l'environnement.",
    ),
)


@checks.register()
def required_settings_check(
    app_configs, **kwargs
):  # pragma: no cover - signature enforced by Django
    errors: list[checks.CheckMessage] = []

    for name, value, error_id, message in REQUIRED_CONFIGURATION:
        if not value:
            errors.append(checks.Critical(message, id=error_id))

    if not settings.DEFAULT_FROM_EMAIL:
        errors.append(
            checks.Critical(
                "DEFAULT_FROM_EMAIL n'est pas défini. Configurez EMAIL_HOST_USER.",
                id="rusard.E005",
            )
        )

    return errors
