from django.shortcuts import render
from .models import Speaker, Sponsor, Schedule


def home_page(request):
    speakers = Speaker.objects.all()
    sponsors = Sponsor.objects.all().order_by("?")
    schedule_day_one = Schedule.objects.filter(day=1).order_by("time")
    schedule_day_two = Schedule.objects.filter(day=2).order_by("time")

    return render(request, 'index-overlay.html', locals())
