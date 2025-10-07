import os

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

PLACEHOLDERS = getattr(settings, "REQUIRED_SETTINGS_PLACEHOLDERS", {})


def _uses_placeholder(name: str, value: str) -> bool:
    placeholder = PLACEHOLDERS.get(name)
    return bool(placeholder) and value == placeholder


@checks.register()
def required_settings_check(
    app_configs, **kwargs
):  # pragma: no cover - signature enforced by Django
    messages: list[checks.CheckMessage] = []

    for name, value, error_id, message in REQUIRED_CONFIGURATION:
        env_value = os.environ.get(name)
        if env_value:
            continue
        if _uses_placeholder(name, value):
            messages.append(
                checks.Warning(
                    f"{message} Une valeur de substitution de développement est utilisée.",
                    id=f"{error_id}.placeholder",
                )
            )
        else:
            messages.append(checks.Critical(message, id=error_id))

    if not settings.DEFAULT_FROM_EMAIL:
        messages.append(
            checks.Critical(
                "DEFAULT_FROM_EMAIL n'est pas défini. Configurez EMAIL_HOST_USER.",
                id="rusard.E005",
            )
        )
    elif _uses_placeholder(
        "EMAIL_HOST_USER", settings.DEFAULT_FROM_EMAIL
    ) and not os.environ.get("EMAIL_HOST_USER"):
        messages.append(
            checks.Warning(
                "DEFAULT_FROM_EMAIL utilise une valeur de substitution. Définissez EMAIL_HOST_USER pour la production.",
                id="rusard.E005.placeholder",
            )
        )

    return messages
