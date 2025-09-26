"""Models for the rusardhome blog."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Article(models.Model):
    """Blog article that can receive comments and likes."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Ensure we generate a unique slug if it is missing."""

        if not self.slug:
            base_slug = slugify(self.title) or "article"
            base_slug = base_slug[:200]
            slug = base_slug
            index = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"[:210]
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """Visitor comment linked to an article."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="article_comments",
    )
    author_name = models.CharField(max_length=150)
    author_email = models.EmailField(blank=True)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Commentaire de {self.author_name} sur {self.article}"


class ArticleLike(models.Model):
    """Represents a visitor's like for an article."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="article_likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "user")

    def __str__(self):
        return f"{self.user} aime {self.article}"
