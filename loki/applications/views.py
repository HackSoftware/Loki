from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import ApplyForm
from .models import (Application, ApplicationInfo,
                     ApplicationProblem, ApplicationProblemSolution)
from website.models import CourseDescription, Snippet
from education.models import Course


@login_required(login_url='website:login')
def apply_course(request, course_url):
    cd = get_object_or_404(CourseDescription, url=course_url)

    try:
        course = cd.course
        if course:
            app_info = ApplicationInfo.objects.get(course=course)
            app_problems = ApplicationProblem.objects.filter(application_info=app_info)
    except (ApplicationInfo.DoesNotExist, ApplicationProblem.DoesNotExist) as err:
        return redirect(reverse('website:profile'))

    if Application.objects.filter(user=request.user).exists():
        return render(request, 'already_applied.html', locals())

    apply_form = ApplyForm(tasks=app_problems.count())

    if request.method == 'POST':
        apply_form = ApplyForm(request.POST, tasks=app_problems.count())

        if apply_form.is_valid():
            application = Application.objects.create(
                user=request.user,
                application_info=app_info,
                phone=apply_form.cleaned_data.get('phone'),
                skype=apply_form.cleaned_data.get('skype'),
                works_at=apply_form.cleaned_data.get('works_at'),
                studies_at=apply_form.cleaned_data.get('studies_at'))

            for index, app_problem in enumerate(app_problems):
                ApplicationProblemSolution.objects.create(
                    application=application,
                    problem=app_problem,
                    solution_url=apply_form.cleaned_data.get('task_{0}'.format(index+1))
                )
            return render(request, 'already_applied.html', locals())
    return render(request, 'apply.html', locals())


@login_required(login_url='website:login')
def apply_overview(request):
    courses = CourseDescription.objects.all().order_by('-course__start_time')
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, 'apply_overview.html', locals())
