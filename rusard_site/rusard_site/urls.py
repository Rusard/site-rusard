"""
URL configuration for rusard_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

import rusardhome.views as views
import ts.views as ts_views
from rusardhome.sitemaps import ArticleSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "articles": ArticleSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.accueil, name="accueil"),
    path("Accueil/", views.accueil, name="accueil"),
    path("Modélisation/", views.modelisation, name="modelisation"),
    path("About/", views.about, name="about"),
    path("ProjetAPP/", views.projetapp, name="projetapp"),
    path("Contact/", views.contact, name="contact"),
    path("ts-tpf/", ts_views.tours_services, name="ts"),
    path("Contact/Confirmation/", views.contactconfirme, name="contactconfirme"),
    path("Mentions-legales/", views.mentions_legales, name="mentions_legales"),
    path(
        "Politique-de-confidentialite/",
        views.politique_confidentialite,
        name="politique_confidentialite",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("auth/", include("social_django.urls", namespace="social")),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.signup, name="signup"),
]
