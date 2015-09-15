from django.contrib import admin

from .models import Speaker, Sponsor, Schedule


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'description', 'facebook', 'twitter', 'google_plus', 'github', 'video_presentation')

    class Meta:
        model = Speaker


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'title')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'name', 'time', 'description', 'speaker', 'co_speaker')


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Speaker, SpeakerAdmin)
