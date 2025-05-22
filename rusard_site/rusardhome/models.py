from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)  # Limite la longueur du titre à 200 caractères
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
