from django.contrib import admin
from hack_fmi.models import BaseUser
from .models import Company, Partner


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

    class Meta:
        model = BaseUser

admin.site.register(BaseUser, BaseUserAdmin)


class CompanyAdmin(admin.ModelAdmin):

    class Meta:
        model = Company

admin.site.register(Company, CompanyAdmin)


class PartnerAdmin(admin.ModelAdmin):

    class Meta:
        model = Partner

admin.site.register(Partner, PartnerAdmin)
