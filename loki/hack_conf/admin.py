from django.contrib import admin

from .models import HackConfUser, Speaker, Sponsor, Schedule


class HackConfUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'datetime')

    class Meta:
        model = HackConfUser


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description', 'facebook', 'twitter', 'google_plus', 'github')

    class Meta:
        model = Speaker


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'name', 'time', 'description', 'author')


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(HackConfUser, HackConfUserAdmin)
