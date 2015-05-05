from django.contrib import admin

from .models import HackConfUser


class HackConfUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'datetime')

    class Meta:
        model = HackConfUser

admin.site.register(HackConfUser, HackConfUserAdmin)
