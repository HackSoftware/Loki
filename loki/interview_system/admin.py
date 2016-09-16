from django.contrib import admin
from django.conf.urls import patterns, url
from .models import Interviewer, InterviewerFreeTime, Interview
from .helpers.interviews import GenerateInterviewSlots, GenerateInterviews


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = ['interviewer',]


@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]

    list_filter = ['date',]


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = [
        'date',
        'start_time',
        'interviewer_time_slot',
        'application',
    ]

    list_filter = ['date',]

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
