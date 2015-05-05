from django.shortcuts import render
from .forms import HackConfUserForm


def email_form_view(request):
    form = HackConfUserForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'thank_you.html')
    return render(request, 'email_form.html')
