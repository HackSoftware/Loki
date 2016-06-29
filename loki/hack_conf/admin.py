from django.contrib import admin

from .models import Speaker, Sponsor, Schedule


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'title',
                    'description',
                    'facebook',
                    'twitter',
                    'google_plus',
                    'github',
                    'video_presentation')


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'website',
                    'title')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day',
                    'name',
                    'time',
                    'description',
                    'speaker',
                    'co_speaker')
