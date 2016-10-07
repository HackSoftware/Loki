from django.contrib import admin

from .models import (Application, ApplicationProblemSolution, ApplicationProblem,
                     ApplicationInfo)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'application_info',
    ]
    search_fields = ['user__email', 'application_info__course__course__name',
                     'has_interview_date']
    list_filter = ['user__email', 'application_info__course__course__name',
                   'has_interview_date']

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(ApplicationProblemSolution)
class ApplicationProblemSolutionAdmin(admin.ModelAdmin):

    list_display = [
        'application',
        'problem',
    ]
    search_fields = ['application__user__email', 'application__user__first_name',
                     'application__application_info__course__course__name']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(ApplicationProblem)
class ApplicationProblemAdmin(admin.ModelAdmin):

    list_display = [
        'name',
    ]

    def has_module_permission(self, request):
        return True


@admin.register(ApplicationInfo)
class ApplicationInfoAdmin(admin.ModelAdmin):

    list_display = [
        'start_date',
        'end_date',
        'course',
    ]

    def has_module_permission(self, request):
        return True
