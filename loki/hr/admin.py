from django.contrib import admin
from .models import HR


class HRAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'company',
    ]
    list_display_links = ['email']

    list_filter = ('company',)

admin.site.register(HR, HRAdmin)
