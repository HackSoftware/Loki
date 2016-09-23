from django.contrib import admin

from .models import (Application, ApplicationProblemSolution, ApplicationProblem,
                     ApplicationInfo)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'application_info',
    ]

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return True

    def has_module_permission(self, request):
        return True


@admin.register(ApplicationProblemSolution)
class ApplicationProblemSolutionAdmin(admin.ModelAdmin):

    list_display = [
        'application',
        'problem',
    ]


@admin.register(ApplicationProblem)
class ApplicationProblemAdmin(admin.ModelAdmin):

    list_display = [
        'name',
    ]


@admin.register(ApplicationInfo)
class ApplicationInfoAdmin(admin.ModelAdmin):

    list_display = [
        'start_date',
        'end_date',
        'course',
    ]
