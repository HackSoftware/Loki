from django.contrib import admin

from .models import Student, Course, CourseAssignment


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
        'works_at',
        'status',
    ]
    list_display_links = ['email']

    list_filter = ('works_at', 'status')

admin.site.register(Student, StudentAdmin)


class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'course',
        'group_time',
        'cv',
        'is_attending',
        'is_online'
    ]

    list_filter = ('course', 'group_time', 'is_attending', 'is_online')
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    list_display_links = ['user']

admin.site.register(CourseAssignment, CourseAssignmentAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    list_display_links = ['name']

admin.site.register(Course, CourseAdmin)
