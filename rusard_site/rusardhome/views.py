import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm

logger = logging.getLogger(__name__)


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
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if not form.is_valid():
            if form.errors.get("website"):
                logger.info("Soumission bloquée par le honeypot anti-spam.")
            messages.error(request, "Le formulaire contient des erreurs.")
        else:
            recaptcha_response = request.POST.get("g-recaptcha-response", "").strip()
            if not recaptcha_response:
                messages.error(
                    request,
                    "Le test reCAPTCHA n'a pas pu être validé. Veuillez réessayer.",
                )
            else:
                data = {
                    "secret": settings.RECAPTCHA_PRIVATE_KEY,
                    "response": recaptcha_response,
                }
                try:
                    verify = requests.post(
                        "https://www.google.com/recaptcha/api/siteverify",
                        data=data,
                        timeout=5,
                    )
                    verify.raise_for_status()
                    result = verify.json()
                except requests.RequestException as exc:
                    logger.warning("Échec de la vérification reCAPTCHA", exc_info=exc)
                    messages.error(
                        request,
                        "Le service de vérification est momentanément indisponible. "
                        "Veuillez réessayer plus tard.",
                    )
                except ValueError as exc:
                    logger.warning("Réponse reCAPTCHA illisible", exc_info=exc)
                    messages.error(
                        request,
                        "Une erreur est survenue avec la vérification. Veuillez réessayer.",
                    )
                else:
                    if not result.get("success") or result.get("score", 0) < 0.5:
                        logger.info(
                            "Vérification reCAPTCHA refusée",
                            extra={"score": result.get("score")},
                        )
                        messages.error(
                            request,
                            "Échec du test reCAPTCHA. Veuillez réessayer.",
                        )
                    else:
                        cleaned = form.cleaned_data
                        full_message = (
                            f"Message de {cleaned['firstname']} {cleaned['name']} "
                            f"({cleaned['email']}):\n\n{cleaned['message']}"
                        )

                        logger.info(
                            "Envoi d'un message de contact réussi",
                            extra={
                                "firstname": cleaned["firstname"],
                                "name": cleaned["name"],
                                "email": cleaned["email"],
                            },
                        )

                        send_mail(
                            subject="Nouveau message du formulaire",
                            message=full_message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=["contact@rusard.ch"],
                        )

                        return redirect("contactconfirme")

    return render(
        request,
        "rusardhome/contact.html",
        {
            "recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY,
            "form": form,
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
