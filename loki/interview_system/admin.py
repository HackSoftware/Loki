from django.contrib import admin

from .models import Interviewer, InterviewerFreeTime, Interview


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
    ]

@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]

    list_filter = ['date',]

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        # print(request.user) TODO: check correctly if user has interviews
        # qs = super(InterviewAdmin, self).get_queryset(request)
        # if qs.filter(interviewer=request.user):
        # interviews = super(InterviewAdmin, self).get_queryset(request)
        # print(interviews)
        # if interviews.filter(interviewer=self):
        return True
        # return False
    def has_module_permission(self, request):
        return True

    list_display = [
        'date',
        'start_time',
        'end_time',
        'application',
    ]

    list_filter = ['date',]
