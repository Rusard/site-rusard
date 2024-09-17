from django.shortcuts import render
from django.http import HttpResponse
from ts.data import data


# Create your views here.


def tours_services(request):
    if request.method == 'POST':
        train_number = request.POST.get('train_number')
        period = request.POST.get('period')

        if not train_number:
            return render(request, 'ts/ts.html', {'error': 'Veuillez entrer un numéro de train.'})

        if not period:
            return render(request, 'ts/ts.html', {'error': 'Veuillez choisir une période de roulement.'})

        try:
            train_number = int(train_number)
        except ValueError:
            return render(request, 'ts/ts.html', {'error': 'Numéro de train invalide. Veuillez entrer un nombre entier.'})


        for tour, trains in data.get(period, {}).items():
            if train_number in trains:
                result = f"N° {train_number} - Effectué par {tour}"
                return render(request, 'ts/ts.html', {'result': result})

        return render(request, 'ts/ts.html', {'error': 'Train non trouvé dans cette période.'})

    return render(request, 'ts/ts.html')

