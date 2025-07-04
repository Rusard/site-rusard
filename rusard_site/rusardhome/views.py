from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def contactconfirme(request):
    return render(request, 'rusardhome/contactconfirme.html')


def accueil(request):
    return render(request, 'rusardhome/accueil.html')


def modelisation(request):
    return render(request, 'rusardhome/modelisation.html')


def about(request):
    return render(request, 'rusardhome/about.html')


def projetapp(request):
    return render(request, 'rusardhome/projetapp.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        honeypot = request.POST.get('website')

        full_message = f"Message de {name} ({email}):\n\n{message}"

        if honeypot:
            full_message += "\n\n[⚠ BOT SUSPECTÉ : champ honeypot rempli]"

        send_mail(
            subject="Nouveau message du formulaire",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["contact@rusard.ch"],  # ← Ton adresse de réception
        )

        return redirect('contactconfirme')
    return render(request, 'rusardhome/contact.html')


def signup(request):
    """Register a new user with the default Django form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})
