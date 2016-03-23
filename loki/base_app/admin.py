from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin

from base_app.models import BaseUser
from .models import Company, Partner, City, GeneralPartner


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'studies_at', 'works_at')

    list_filter = ('is_active',)
    search_fields = ['email', 'first_name', 'last_name', 'studies_at', 'works_at']

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


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = City

admin.site.register(City, CityAdmin)
admin.site.register(GeneralPartner)
