from django.shortcuts import render
from .forms import HackConfUserForm
from .models import Speaker, Sponsor


def home_page(request):
    speakers = Speaker.objects.all()
    sponsors = Sponsor.objects.all()
    return render(
        request,
        'index-overlay.html',
        {
            'speakers': speakers,
            'sponsors': sponsors,
        }
    )


def email_form_view(request):
    form = HackConfUserForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'thank_you.html')
    return render(request, 'register.html')


