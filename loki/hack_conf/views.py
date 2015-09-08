from django.shortcuts import render
from .models import Speaker, Sponsor, Schedule


def home_page(request):
    speakers = Speaker.objects.all()

    sponsors_silver = Sponsor.objects.filter(title=Sponsor.SPONSOR_SILVER).order_by("?")
    sponsors_gold = Sponsor.objects.filter(title=Sponsor.SPONSOR_GOLD).order_by("?")
    sponsors_platinum = Sponsor.objects.filter(title=Sponsor.SPONSOR_PLATINUM).order_by("?")

    general_media_partners = Sponsor.objects.filter(
        title=Sponsor.GENERAL_MEDIA_PARTNER
    ).order_by("?")
    branch_partners = Sponsor.objects.filter(title=Sponsor.BRANCH_PARTNER).order_by("?")
    media_partners = Sponsor.objects.filter(title=Sponsor.MEDIA_PARTNER).order_by("?")
    school_partners = Sponsor.objects.filter(title=Sponsor.SCHOOL_PARTNER).order_by("?")

    schedule_day_one = Schedule.objects.filter(day=1).order_by("time")
    schedule_day_two = Schedule.objects.filter(day=2).order_by("time")

    return render(request, 'index.html', locals())
