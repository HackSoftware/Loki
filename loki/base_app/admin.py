from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin

from hack_fmi.models import BaseUser
from .models import Company, Partner, Event, Ticket, City
from .modelresource import TicketResource


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


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date')

    class Meta:
        model = Event

admin.site.register(Event, EventAdmin)


class TicketAdmin(ImportExportActionModelAdmin):
    resource_class = TicketResource

    def full_name(self, obj):
        return obj.base_user.full_name

    def birth_place(self, obj):
        return obj.base_user.birth_place

    def description(self, obj):
        return obj.base_user.description

    list_display = ('id', 'event', 'full_name', 'birth_place', 'description')

    class Meta:
        model = Ticket

    list_filter = ('event',)

admin.site.register(Ticket, TicketAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        model = City

admin.site.register(City, CityAdmin)
