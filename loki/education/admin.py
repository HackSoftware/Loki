from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin, messages

from .modelresource import StudentResource, CourseAssignmentResource, WorkingAtResource
from .models import (Student, Course, CourseAssignment, Teacher, Lecture, CheckIn, StudentNote,
                     WorkingAt, Task, Solution, Certificate, ProgrammingLanguage, Test,
                     GraderRequest, RetestSolution)


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


class CourseAssignmentAdmin(ImportExportActionModelAdmin):
    resource_class = CourseAssignmentResource

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


class WorkingAtAdmin(ImportExportActionModelAdmin):
    resource_class = WorkingAtResource

    list_display = [
        'full_name',
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
    search_fields = [
        'student__email',
        'company_name',
        'company__name',
        'student__first_name',
        'student__last_name',
    ]

    def full_name(self, obj):
        return obj.student.full_name

admin.site.register(WorkingAt, WorkingAtAdmin)


class TaskAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'course',
        'week',
        'gradable',
        'submited_solutions'
    ]

    list_filter = [
        'course',
        'week',
    ]

    search_fields = ['course__name', 'name', 'week']

    def submited_solutions(self, task):
        return len(task.solution_set.all())

admin.site.register(Task, TaskAdmin)


class ProgrammingLanguageAdmin(admin.ModelAdmin):

    list_display = [
        'name',
    ]

    list_filter = [
        'name',
    ]

    search_fields = ['name']

admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)


class TestAdmin(admin.ModelAdmin):

    list_display = [
        'task',
        'language',
        'test_type',
    ]

    list_filter = [
        'language',
        'test_type',
    ]

    search_fields = ['task']

admin.site.register(Test, TestAdmin)


class SolutionAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if (obj.code is None or obj.code == "") and (obj.url is None or obj.url == ""):
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Url or Code should be given.')
            return
        else:
            obj.save()

    def get_solution_course(self, obj):
        return obj.task.course
    get_solution_course.short_description = "Course"
    get_solution_course.admin_order_field = "task__course"

    list_filter = [
        'status'
    ]

    readonly_fields = [
        'task',
        'student',
        'url',
        'code',
        'build_id',
        'check_status_location',
        'status',
        'test_output',
        'return_code',
    ]

    list_display = [
        'id',
        'task',
        'status',
        'student',
        'get_solution_course',
        'url',
    ]

    list_filter = [
        'task',
    ]

    search_fields = ['id', 'task__name', 'student__first_name']

admin.site.register(Solution, SolutionAdmin)

admin.site.register(Certificate)


class GraderRequestAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'request_info',
        'nonce',
    ]

    list_filter = [
        'request_info',
    ]

    search_fields = ['nonce']

admin.site.register(GraderRequest, GraderRequestAdmin)


class RetestSolutionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'status',
        'date',
        'test_id',
        'tested_solutions_count',
    ]

    list_filter = [
        'status',
    ]

    search_fields = ['test_id']

admin.site.register(RetestSolution, RetestSolutionAdmin)
