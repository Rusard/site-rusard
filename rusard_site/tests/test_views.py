import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_accueil_view(client):
    url = reverse('accueil')
    response = client.get(url)
    assert response.status_code == 200
