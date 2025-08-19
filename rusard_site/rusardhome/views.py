import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def contactconfirme(request):
    return render(request, "rusardhome/contactconfirme.html")


def accueil(request):
    return render(request, "rusardhome/accueil.html")


def modelisation(request):
    return render(request, "rusardhome/modelisation.html")


def about(request):
    return render(request, "rusardhome/about.html")


def projetapp(request):
    return render(request, "rusardhome/projetapp.html")


def mentions_legales(request):
    return render(request, "rusardhome/mentions_legales.html")


def politique_confidentialite(request):
    return render(request, "rusardhome/politique_confidentialite.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        honeypot = request.POST.get("website")

        # Vérification des champs obligatoires
        if not name or not email or not message:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(
                request,
                "rusardhome/contact.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY,
                    "name": name,
                    "email": email,
                    "message": message,
                },
            )

        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": recaptcha_response,
        }
        verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        )
        result = verify.json()
        # Vérification du score reCAPTCHA v3
        if not result.get("success") or result.get("score", 0) < 0.5:
            messages.error(request, "Échec du test reCAPTCHA. Veuillez réessayer.")
            return render(
                request,
                "rusardhome/contact.html",
                {
                    "recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY,
                    "name": name,
                    "email": email,
                    "message": message,
                },
            )

        full_message = f"Message de {name} ({email}):\n\n{message}"

        if honeypot:
            full_message += "\n\n[⚠ BOT SUSPECTÉ : champ honeypot rempli]"

        send_mail(
            subject="Nouveau message du formulaire",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["contact@rusard.ch"],  # ← Ton adresse de réception
        )

        return redirect("contactconfirme")
    return render(
        request,
        "rusardhome/contact.html",
        {
            "recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY,
            "name": "",
            "email": "",
            "message": "",
        },
    )


def signup(request):
    """Register a new user with the default Django form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accueil")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
