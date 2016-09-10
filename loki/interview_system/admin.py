from django.contrib import admin

from .models import Interviewer, InterviewerFreeTime, Interview


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
    ]

@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = [
        'start_time',
        'end_time',
    ]
