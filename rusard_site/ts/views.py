import logging

from django.shortcuts import render
from ts.data import data

logger = logging.getLogger(__name__)

HISTORY_SESSION_KEY = "ts_history"
PERIOD_CHOICES = (
    ("Lundi-Jeudi", "Lundi-Jeudi"),
    ("Vendredi", "Vendredi"),
    ("Samedi", "Samedi"),
    ("Dimanche", "Dimanche"),
)


# Create your views here.


def tours_services(request):
    context = {
        "history": request.session.get(HISTORY_SESSION_KEY, []),
        "train_number": "",
        "period": "",
        "period_choices": PERIOD_CHOICES,
    }

    if request.method == "POST":
        train_number_raw = request.POST.get("train_number", "").strip()
        period = request.POST.get("period", "").strip()

        context.update(
            {
                "train_number": train_number_raw,
                "period": period,
            }
        )

        if not train_number_raw:
            context["error"] = "Veuillez entrer un numéro de train."
            return render(request, "ts/ts.html", context)

        if not period:
            context["error"] = "Veuillez choisir une période de roulement."
            return render(request, "ts/ts.html", context)

        try:
            train_number = int(train_number_raw)
        except ValueError:
            context["error"] = (
                "Numéro de train invalide. Veuillez entrer un nombre entier."
            )
            return render(request, "ts/ts.html", context)

        for tour, trains in data.get(period, {}).items():
            if train_number in trains:
                result = f"N° {train_number} - Effectué par {tour}"
                context["result"] = result

                history = [
                    {
                        "train_number": train_number,
                        "period": period,
                        "tour": tour,
                    }
                ]
                history.extend(request.session.get(HISTORY_SESSION_KEY, []))
                request.session[HISTORY_SESSION_KEY] = history[:5]
                request.session.modified = True

                logger.info(
                    "Consultation de tour de service",
                    extra={
                        "train_number": train_number,
                        "period": period,
                        "tour": tour,
                    },
                )

                context["history"] = request.session[HISTORY_SESSION_KEY]
                return render(request, "ts/ts.html", context)

        logger.info(
            "Train non trouvé", extra={"train_number": train_number, "period": period}
        )
        context["error"] = "Train non trouvé dans cette période."
        return render(request, "ts/ts.html", context)

    return render(request, "ts/ts.html", context)
