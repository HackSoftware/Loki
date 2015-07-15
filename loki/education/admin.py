from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin

from .models import Student, Course, CourseAssignment, Teacher, Lecture, CheckIn, StudentNote, WorkingAt
from .modelresource import StudentResource


class StudentAdmin(ImportExportActionModelAdmin):
    resource_class = StudentResource

    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
        'github_account',
        'get_courses',
        'is_active',
    ]
    list_display_links = ['email']
    list_filter = ('courses', 'is_active')
    search_fields = ['email', 'first_name', 'last_name', 'mac', 'github_account']

    def get_courses(self, obj):
        return obj.courses.all()

admin.site.register(Student, StudentAdmin)


class StudentNoteAdmin(admin.ModelAdmin):
    list_display = [
        'assignment',
        'author',
        'post_time',
    ]

    list_display_links = ['assignment']

admin.site.register(StudentNote, StudentNoteAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
    ]
    list_display_links = ['email']

admin.site.register(Teacher, TeacherAdmin)


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


class LectureAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'course'
    ]

admin.site.register(Lecture, LectureAdmin)


class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'mac',
        'student'
    ]
    search_fields = ['mac', 'student__email']

admin.site.register(CheckIn, CheckInAdmin)


class WorkingAtAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'company',
        'company_name',
        'course',
        'came_working',
        'location',
        'start_date',
        'end_date',
        'title',
        'description',
    ]
    search_fields = ['company', 'location', 'student', 'course']

admin.site.register(WorkingAt, WorkingAtAdmin)
