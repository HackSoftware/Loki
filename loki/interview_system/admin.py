from django.contrib import admin
from .models import Interviewer, InterviewerFreeTime, Interview


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = ['interviewer', ]

    def has_module_permission(self, request):
        return True


@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]
    search_fields = ['interviewer__email', 'interviewer__first_name']
    list_filter = ['date', ]

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = [
        'date',
        'uuid',
        'start_time',
        'interviewer',
        'view_application',
        'has_confirmed'
    ]
    search_fields = ['interviewer__email', 'interviewer__first_name', 'date']
    list_filter = ['date', 'start_time']

    def view_application(self, obj):
        return obj.application

    view_application.empty_value_display = 'Free Slot'
    view_application.short_description = "Applications"

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
