from django.contrib import admin
from .models import Interviewer, InterviewerFreeTime, Interview


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = ['interviewer', ]


@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]

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
        'interviewer',
        'start_time',
        'application',
        'uuid',
        'has_confirmed'
    ]

    list_filter = ['date']

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
