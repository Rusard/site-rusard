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

import rusardhome.views as views
import ts.views as ts_views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from rusardhome.sitemaps import ArticleSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "articles": ArticleSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.accueil, name="accueil"),
    path("accueil/", views.accueil, name="accueil"),
    path("modelisation/", views.modelisation, name="modelisation"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("blog/<slug:slug>/like/", views.blog_toggle_like, name="blog_toggle_like"),
    path("about/", views.about, name="about"),
    path("projetapp/", views.projetapp, name="projetapp"),
    path("contact/", views.contact, name="contact"),
    path("ts-tpf/", ts_views.tours_services, name="ts"),
    path("contact/confirmation/", views.contactconfirme, name="contactconfirme"),
    path("mentions-legales/", views.mentions_legales, name="mentions_legales"),
    path(
        "politique-de-confidentialite/",
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


legacy_uppercase_patterns = [
    (r"^Accueil/$", "accueil"),
    (r"^Mod[ée]lisation/$", "modelisation"),
    (r"^Blog/$", "blog_list"),
    (r"^Blog/(?P<slug>[^/]+)/$", "blog_detail"),
    (r"^Blog/(?P<slug>[^/]+)/like/$", "blog_toggle_like"),
    (r"^About/$", "about"),
    (r"^ProjetAPP/$", "projetapp"),
    (r"^Contact/$", "contact"),
    (r"^Contact/Confirmation/$", "contactconfirme"),
    (r"^Mentions_legales/$", "mentions_legales"),
    (r"^Politique_de_confidentialite/$", "politique_confidentialite"),
]


for pattern, target_name in legacy_uppercase_patterns:
    urlpatterns.append(
        re_path(
            pattern,
            RedirectView.as_view(pattern_name=target_name, permanent=True),
        )
    )
