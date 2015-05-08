from django.shortcuts import render
from .forms import HackConfUserForm


def home_page(request):
    return render(request, 'index-overlay.html')


def email_form_view(request):
    form = HackConfUserForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'thank_you.html')
    return render(request, 'register.html')


