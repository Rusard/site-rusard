from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article  # ou un autre modèle de ton site


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'accueil',
            'modelisation',
            'contact',
            'blog_list',
            'about',
            'projetapp',
            'contactconfirme',
            'ts',
        ]  # noms des vues `name=` dans urls.py

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # assure-toi que ton modèle a un champ `updated_at`
