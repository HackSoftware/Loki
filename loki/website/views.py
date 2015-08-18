from django.shortcuts import render
from .models import Successor, SuccessViedeo, Snippet

from base_app.models import Partner


def index(request):
    successors = Successor.objects.order_by('?')[:6]
    partners = Partner.objects.all()[:6]
    videos = SuccessViedeo.objects.all()[:4]
    success_counter = 98
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/index.html", locals())
