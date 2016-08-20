from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import SuccessVideo, SuccessStoryPerson, Snippet, CourseDescription

from education.models import WorkingAt, Student, Teacher, Course
from base_app.models import Partner, GeneralPartner, BaseUser
from base_app.services import send_activation_mail, send_forgotten_password_email
from base_app.helper import get_or_none
from applications.forms import ApplyForm
from applications.models import (Application, ApplicationInfo,
                                 ApplicationProblem, ApplicationProblemSolution)

from .forms import (RegisterForm, LoginForm, BaseEditForm, StudentEditForm,
                    TeacherEditForm)
from .decorators import anonymous_required
from easy_thumbnails.files import get_thumbnailer


def index(request):
    successors = SuccessStoryPerson.objects.filter(show_picture_on_site=True).order_by('?')[:6]
    partners = Partner.objects.all().order_by('?')
    videos = SuccessVideo.objects.all()[:4]

    success = WorkingAt.objects.filter(came_working=False)
    success_students = map(lambda x: x.student, success)
    success_students_count = len(set(success_students))

    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/index.html", locals())


def about(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    return render(request, "website/about.html", locals())


def courses(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    courses = CourseDescription.objects.all().order_by('-course__start_time')
    return render(request, "website/courses.html", locals())


def partners(request):
    general_partners = GeneralPartner.objects.all().order_by('?')
    general_partners = [gp.partner for gp in general_partners]
    partners = Partner.objects.all().order_by('?')
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/partners.html", locals())


def course_details(request, course_url):
    # cd refers to course_description
    cd = get_object_or_404(CourseDescription, url=course_url)
    teachers = cd.course.teacher_set.all()
    partners = cd.course.partner.all().order_by('?')
    course_days = " ".join([word.strip() for word in cd.course_days.split(",")])
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/course_details.html", locals())


@anonymous_required(redirect_url=reverse_lazy('website:profile'))
def register(request):
    origin = request.GET.get('origin', None)
    form = RegisterForm(initial={'origin': origin})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_mail(request, user)
            return render(request, 'website/auth/thanks.html')
    return render(request, "website/auth/register.html", locals())


@anonymous_required(redirect_url=reverse_lazy('website:profile'))
def log_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('website:index'))
                else:
                    error = "Моля активирай акаунта си"
            else:
                error = "Невалидни email и/или парола"
    return render(request, "website/auth/login.html", locals())


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('website:index'))


@login_required(login_url='website:login')
def profile(request):
    user = BaseUser.objects.get(email=request.user.email)
    try:
        student = Student.objects.get(email=request.user.email)
    except Student.DoesNotExist:
        student = None
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except Teacher.DoesNotExist:
        teacher = None
    return render(request, 'website/profile.html', locals())


@login_required(login_url='website:login')
def profile_edit(request):
    base_form = BaseEditForm(instance=request.user)

    if request.method == 'POST':
        base_form = BaseEditForm(request.POST, request.FILES, instance=request.user)

        if base_form.is_valid():
            base_form.save()
        else:
            errors = base_form.errors

    return render(request, "website/profile_edit.html", locals())


@login_required(login_url='website:login')
def profile_edit_student(request):
    try:
        student = Student.objects.get(email=request.user.email)
    except Student.DoesNotExist:
        return redirect(reverse('website:profile'))
    student_form = StudentEditForm(instance=student)

    if request.method == 'POST':
        student_form = StudentEditForm(request.POST, request.FILES,
                                       instance=student)
        if student_form.is_valid():
            student_form.save()
            if Teacher.objects.filter(email=request.user.email).exists():
                teacher = Teacher.objects.get(email=request.user.email)
                TeacherEditForm(request.POST, request.FILES,
                                instance=teacher).save()
        else:
            errors = student_form.errors
            return render(request, "website/profile_edit_student.html", locals())
    return render(request, 'website/profile_edit_student.html', locals())


@login_required(login_url='website:login')
def profile_edit_teacher(request):
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except Teacher.DoesNotExist:
        return redirect(reverse('website:profile'))
    teacher_form = TeacherEditForm(instance=teacher)

    if request.method == 'POST':
        teacher_form = TeacherEditForm(request.POST, request.FILES,
                                       instance=teacher)
        if teacher_form.is_valid():
            teacher_form.save()
            if Student.objects.filter(email=request.user.email).exists():
                student = Student.objects.get(email=request.user.email)
                StudentEditForm(request.POST, request.FILES,
                                instance=student).save()
        else:
            errors = teacher_form.errors
            return render(request, "website/profile_edit_teacher.html", locals())
    return render(request, 'website/profile_edit_teacher.html', locals())


def forgotten_password(request):
    if request.POST:
        email = request.POST.get('email', '').strip()
        baseuser = get_or_none(BaseUser, email=email)
        if baseuser is None:
            message = "Потребител с посочения email не е открит"
        else:
            message = "Email за промяна на паролата беше изпратен на посочения адрес"
            send_forgotten_password_email(request, baseuser)
    return render(request, 'website/auth/forgotten_password.html', locals())

@login_required(login_url='website:login')
def apply_overview(request):
    return render(request, 'website/application/apply_overview.html', locals())


@login_required(login_url='website:login')
def apply_course(request, course_url):
    cd = get_object_or_404(CourseDescription, url=course_url)

    try:
        course = Course.objects.get(url=course_url)
        if course:
            app_info = ApplicationInfo.objects.get(course=course)
            app_problems = ApplicationProblem.objects.filter(application_info=app_info)
    except (ApplicationInfo.DoesNotExist, Course.DoesNotExist,
            ApplicationProblem.DoesNotExist) as err:
        return redirect(reverse('website:profile'))

    if Application.objects.filter(user=request.user).exists():
        return render(request, 'website/application/already_applied.html', locals())

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
            application.save()
            for index, app_problem in enumerate(app_problems):
                ApplicationProblemSolution.objects.create(
                    application=application,
                    problem=app_problem,
                    solution_url=apply_form.cleaned_data.get('task_{0}'.format(index+1))
                ).save()
            return render(request, 'website/application/already_applied.html', locals())
    return render(request, 'website/application/apply.html', locals())
