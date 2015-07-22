from django.shortcuts import render
from .models import Successor


def index(request):
    successors = Successor.objects.all()
    success_counter = 98
    return render(request, "website/index.html", locals())
