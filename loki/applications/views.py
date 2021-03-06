from django.http import HttpResponseForbidden
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from loki.website.models import CourseDescription, Snippet
from loki.emails.services import send_template_email

from .forms import ApplyForm
from .models import Application, ApplicationInfo, ApplicationProblem, ApplicationProblemSolution


class ApplyCourseView(LoginRequiredMixin, View):
    """
    Right now we are using View because we want to flash message using
    django messages. This is very hard for function-based views & decorators.

    TODO: Make it a FormView & DRY it a bit.
    """
    def get_login_url(self):
        return reverse('website:login')

    def handle_no_permission(self):
        messages.warning(self.request, 'За да кандидатстваш, трябва да имаш регистрацията в системата.')

        return super().handle_no_permission()

    def get(self, request, course_url):
        cd = get_object_or_404(CourseDescription, url=course_url)
        course = cd.course
        app_info = cd.applicationinfo

        if not app_info.apply_is_active():
            messages.warning(request, 'Срокът за кандидатстване за {} е изтекъл.'.format(course.name))
            return redirect(reverse('applications:apply_overview'))

        app_problems = ApplicationProblem.objects.filter(application_info=app_info)

        if Application.objects.filter(user=request.user, application_info=app_info).exists():
            messages.warning(request, 'Вече си кандидатствал/а за този курс. Може да редактираш своята кандидатура')
            return redirect(reverse('applications:edit_application', args=(cd.url, )))

        apply_form = ApplyForm(tasks=app_problems.count(), app_problems=app_problems)
        problems = list(range(len(apply_form.fields) - len(app_problems))) + list(app_problems)

        return render(request, 'apply.html', locals())

    def post(self, request, course_url):
        cd = get_object_or_404(CourseDescription, url=course_url)
        course = cd.course
        app_info = cd.applicationinfo

        if not app_info.apply_is_active():
            return HttpResponseForbidden('Не можеш да кандидатстваш за изтекъл курс')

        app_problems = ApplicationProblem.objects.filter(application_info=app_info)

        if Application.objects.filter(user=request.user, application_info=app_info).exists():
            return redirect(reverse('applications:edit_applications'))

        apply_form = ApplyForm(tasks=app_problems.count(), app_problems=app_problems)
        problems = list(range(len(apply_form.fields) - len(app_problems))) + list(app_problems)

        if request.method == 'POST':
            apply_form = ApplyForm(request.POST,
                                   tasks=app_problems.count(),
                                   app_problems=app_problems)

            if apply_form.is_valid():
                apply_form.save(app_info, app_problems, request.user)
                messages.success(request, 'Кандидатурата ти е успешно приета. Можеш да я редактираш от профила си')

                context = {
                    'full_name': request.user.full_name,
                    'course_name': course.name
                }

                # TODO: Add ability to set custom template from the model
                email_template = settings.EMAIL_TEMPLATES['application_completed_default']
                send_template_email(request.user.email, email_template, context)
                return redirect(reverse('applications:edit_applications'))

        return render(request, 'apply.html', locals())


def apply_overview(request):
    apply_courses = [info.course for info in ApplicationInfo.objects.get_open_for_apply()]

    """
    TODO: Handle in html if there are no current courses to apply
    """

    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, 'apply_overview.html', locals())


@login_required(login_url='website:login')
def edit_applications(request):
    course_descriptions = [application.application_info.course
                           for application
                           in Application.objects.filter(user=request.user)]
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, 'edit_applications.html', locals())


@login_required(login_url='website:login')
def edit_application(request, course_url):
    cd = get_object_or_404(CourseDescription, url=course_url)
    course = cd.course
    app_info = ApplicationInfo.objects.get(course=cd)
    user_application = Application.objects.get(user=request.user, application_info=app_info)

    initial_data = {'phone': user_application.phone,
                    'skype': user_application.skype,
                    'works_at': user_application.works_at,
                    'studies_at': user_application.studies_at}

    app_problems = user_application.application_info.applicationproblem_set.all()

    for index, problem in enumerate(app_problems):
        solution = ApplicationProblemSolution.objects.filter(application=user_application, problem=problem)

        if not solution.exists():
            continue

        initial_data['task_{0}'.format(index+1)] = solution.first().solution_url

    apply_form = ApplyForm(tasks=app_problems.count(),
                           app_problems=app_problems,
                           initial=initial_data)

    if request.method == 'POST':
        apply_form = ApplyForm(request.POST,
                               tasks=app_problems.count(),
                               app_problems=app_problems,
                               initial=initial_data)
        if apply_form.is_valid():
            apply_form.update(user_application.application_info, app_problems, request.user)
            messages.success(request, 'Успешно обнови кандидатурата си.')
            return redirect(reverse('applications:edit_applications'))

    return render(request, 'edit_application.html', locals())
