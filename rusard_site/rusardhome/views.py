from django.shortcuts import render


def accueil(request):
    return render(request, 'rusardhome/accueil.html')


def modelisation(request):
    return render(request, 'rusardhome/modelisation.html')


def about(request):
    return render(request, 'rusardhome/about.html')


def projetapp(request):
    return render(request, 'rusardhome/projetapp.html')


def contact(request):
    return render(request, 'rusardhome/contact.html')
