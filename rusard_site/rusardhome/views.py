from django.shortcuts import render


def home(request):
    return render(request, 'rusardhome/home.html')


def modelisation(request):
    return render(request, 'rusardhome/modelisation.html')
