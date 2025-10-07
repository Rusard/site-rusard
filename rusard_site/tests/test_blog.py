import pytest
from django.urls import reverse
from rusardhome.models import Article, ArticleLike, Comment


@pytest.mark.django_db
def test_blog_list_displays_articles(client):
    article = Article.objects.create(title="Premier article", content="Contenu de test")

    response = client.get(reverse("blog_list"))

    assert response.status_code == 200
    assert article.title in response.content.decode()


@pytest.mark.django_db
def test_blog_detail_allows_comment_submission(client):
    article = Article.objects.create(title="Article", content="Contenu")
    url = article.get_absolute_url()

    response = client.post(
        url,
        {
            "author_name": "Alice",
            "author_email": "alice@example.com",
            "body": "Super article !",
            "comment_submit": "1",
        },
    )

    assert response.status_code == 302
    assert response["Location"].endswith("#comments")
    assert Comment.objects.filter(
        article=article, body__icontains="Super article"
    ).exists()


@pytest.mark.django_db
def test_authenticated_comment_uses_user_identity(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="john",
        password="password123",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
    )
    article = Article.objects.create(title="Article", content="Contenu")

    assert client.login(username="john", password="password123")

    response = client.post(
        article.get_absolute_url(),
        {
            "author_name": "Anonyme",
            "author_email": "anon@example.com",
            "body": "Commentaire authentifié",
            "comment_submit": "1",
        },
    )

    comment = Comment.objects.get(article=article)
    assert response.status_code == 302
    assert comment.user == user
    assert comment.author_name == "John Doe"
    assert comment.author_email == "john@example.com"


@pytest.mark.django_db
def test_toggle_like_creates_and_removes_like(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="likeuser",
        password="password123",
    )
    article = Article.objects.create(title="Aimer", content="Contenu")

    toggle_url = reverse("blog_toggle_like", args=[article.slug])

    # Non authentifié redirigé vers la connexion
    response = client.post(toggle_url)
    assert response.status_code == 302
    assert response["Location"].startswith(reverse("login"))

    assert client.login(username="likeuser", password="password123")

    response = client.post(toggle_url)
    assert response.status_code == 302
    assert ArticleLike.objects.filter(article=article, user=user).exists()

    response = client.post(toggle_url)
    assert response.status_code == 302
    assert not ArticleLike.objects.filter(article=article, user=user).exists()
