import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_accueil_view(client):
    url = reverse("accueil")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_mentions_legales_view(client):
    url = reverse("mentions_legales")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_politique_confidentialite_view(client):
    url = reverse("politique_confidentialite")
    response = client.get(url)
    assert response.status_code == 200
