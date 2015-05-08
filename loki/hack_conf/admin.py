from django.contrib import admin

from .models import HackConfUser, Speaker


class HackConfUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'datetime')

    class Meta:
        model = HackConfUser


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'facebook', 'twitter', 'google_plus', 'github')

    class Meta:
        model = Speaker

admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(HackConfUser, HackConfUserAdmin)
