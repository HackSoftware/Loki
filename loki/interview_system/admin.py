from django.contrib import admin

from .models import Interviewer, InterviewerFreeTime, Interview
from .utils import render_template_with_context
from .decorators import func_args


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
        'start_time',
        'get_interviewer',
        'get_applying_student',
        'get_student_email',
        'get_student_skype',
        'get_student_phone',
        'get_student_application_course',
        'has_received_email',
        'get_interview_confirmation',
        'get_tasks',
        'get_code_skills',
        'get_code_design',
        'get_fit_attitude',
        'is_accepted',
    ]
    search_fields = ['interviewer__email', 'interviewer__first_name', 'date']
    list_filter = ['date', 'start_time']

    @func_args(short_description='Interviewer')
    def get_interviewer(self, obj):
        return obj.interviewer.full_name

    @func_args(short_description='Student', empty_value_display='Free slot', allow_tags=True)
    def get_applying_student(self, obj):
        """
        Allows easier checking of the student's profile.
        The returned output is clickable link - student's profile.
        """
        if not obj.application:
            return

        context = {
            'base_user_id': obj.application.user.id,
            'student_name': obj.application.user.full_name
        }
        student_html = 'interview_system/templates/partial/interview_student.html'

        return render_template_with_context(target_html=student_html,
                                            context=context)

    @func_args(short_description='Student email', empty_value_display='Free slot')
    def get_student_email(self, obj):
        if not obj.application:
            return

        return obj.application.user.email

    @func_args(short_description='Student skype', empty_value_display='Free slot')
    def get_student_skype(self, obj):
        if not obj.application:
            return

        return obj.application.skype

    @func_args(short_description='Student phone', empty_value_display='Free slot')
    def get_student_phone(self, obj):
        if not obj.application:
            return

        return obj.application.phone

    @func_args(short_description='Applying for', empty_value_display='Free slot')
    def get_student_application_course(self, obj):
        if not obj.application:
            return

        return obj.application.application_info

    @func_args(short_description='Confirmed interview', boolean=True)
    def get_interview_confirmation(self, obj):
        return obj.has_confirmed

    @func_args(short_description='Solutions', allow_tags=True)
    def get_tasks(self, obj):
        """
        Allows easier checking of student's course problem solutions.
        The returned output is ordered list with clickable list items - solutions.
        """
        if not obj.application:
            return

        context = {'tasks': []}
        solution_html = 'interview_system/templates/partial/solution_element.html'
        problems = obj.application.application_info.applicationproblem_set.all()

        for problem in problems:
            solution = obj.application.applicationproblemsolution_set\
                          .filter(problem=problem).first()

            if not solution:
                continue

            task_data = {
                'url': solution.solution_url,
                'name': problem.name
            }
            context['tasks'].append(task_data)

        return render_template_with_context(target_html=solution_html,
                                            context=context)

    @func_args(short_description='Code skills')
    def get_code_skills(self, obj):
        return obj.code_skills_rating

    @func_args(short_description='Code design')
    def get_code_design(self, obj):
        return obj.code_design_rating

    @func_args(short_description='Fit attitude')
    def get_fit_attitude(self, obj):
        return obj.fit_attitude_rating

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
