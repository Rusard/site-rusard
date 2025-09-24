import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_tours_services_success(client):
    response = client.post(
        reverse("ts"),
        data={"train_number": "14267", "period": "Lundi-Jeudi"},
    )

    assert response.status_code == 200
    assert "Effectué par Ts4551" in response.content.decode()

    session = client.session
    history = session.get("ts_history")
    assert history
    assert history[0]["train_number"] == 14267
    assert history[0]["tour"] == "Ts4551"


@pytest.mark.django_db
def test_tours_services_invalid_number(client):
    response = client.post(
        reverse("ts"),
        data={"train_number": "abc", "period": "Lundi-Jeudi"},
    )

    assert response.status_code == 200
    assert "Numéro de train invalide" in response.content.decode()


@pytest.mark.django_db
def test_tours_services_unknown_train(client):
    response = client.post(
        reverse("ts"),
        data={"train_number": "99999", "period": "Vendredi"},
    )

    assert response.status_code == 200
    assert "Train non trouvé" in response.content.decode()
