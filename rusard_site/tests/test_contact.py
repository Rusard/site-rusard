import pytest
import requests
from django.urls import reverse


@pytest.fixture
def recaptcha_success(monkeypatch):
    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self._payload

    def fake_post(url, data=None, timeout=None):
        assert url == "https://www.google.com/recaptcha/api/siteverify"
        assert timeout == 5
        return DummyResponse({"success": True, "score": 0.9})

    monkeypatch.setattr("rusardhome.views.requests.post", fake_post)


@pytest.mark.django_db
def test_contact_form_success(client, settings, recaptcha_success, monkeypatch):
    settings.RECAPTCHA_PRIVATE_KEY = "private"
    settings.RECAPTCHA_PUBLIC_KEY = "public"
    settings.DEFAULT_FROM_EMAIL = "from@example.com"

    sent = {}

    def fake_send_mail(*args, **kwargs):
        sent["called"] = True
        return 1

    monkeypatch.setattr("rusardhome.views.send_mail", fake_send_mail)

    response = client.post(
        reverse("contact"),
        data={
            "firstname": "Jean",
            "name": "Dupont",
            "email": "jean.dupont@example.com",
            "message": "Bonjour",
            "g-recaptcha-response": "token",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("contactconfirme")
    assert sent.get("called") is True


@pytest.mark.django_db
def test_contact_form_honeypot_blocks_send(
    client, settings, recaptcha_success, monkeypatch
):
    settings.RECAPTCHA_PRIVATE_KEY = "private"
    settings.RECAPTCHA_PUBLIC_KEY = "public"
    settings.DEFAULT_FROM_EMAIL = "from@example.com"

    def fake_send_mail(*args, **kwargs):  # pragma: no cover - safety net
        raise AssertionError("send_mail ne devrait pas être appelé")

    monkeypatch.setattr("rusardhome.views.send_mail", fake_send_mail)

    response = client.post(
        reverse("contact"),
        data={
            "firstname": "Jean",
            "name": "Dupont",
            "email": "jean.dupont@example.com",
            "message": "Bonjour",
            "website": "bot",
            "g-recaptcha-response": "token",
        },
    )

    assert response.status_code == 200
    content = response.content.decode()
    assert "Le formulaire contient des erreurs." in content


@pytest.mark.django_db
def test_contact_form_recaptcha_network_error(client, settings, monkeypatch):
    settings.RECAPTCHA_PRIVATE_KEY = "private"
    settings.RECAPTCHA_PUBLIC_KEY = "public"
    settings.DEFAULT_FROM_EMAIL = "from@example.com"

    def fake_post(*args, **kwargs):
        raise requests.RequestException()

    monkeypatch.setattr("rusardhome.views.requests.post", fake_post)

    response = client.post(
        reverse("contact"),
        data={
            "firstname": "Jean",
            "name": "Dupont",
            "email": "jean.dupont@example.com",
            "message": "Bonjour",
            "g-recaptcha-response": "token",
        },
    )

    assert response.status_code == 200
    assert (
        "Le service de vérification est momentanément indisponible"
        in response.content.decode()
    )
