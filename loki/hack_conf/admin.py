from django.contrib import admin

from .models import HackConfUser, Speaker, Sponsor


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


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(HackConfUser, HackConfUserAdmin)
