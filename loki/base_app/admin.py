from django.contrib import admin
from hack_fmi.models import BaseUser


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

    class Meta:
        model = BaseUser
