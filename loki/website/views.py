from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import SuccessVideo, SuccessStoryPerson, Snippet, CourseDescription

from education.models import WorkingAt
from base_app.models import Partner, GeneralPartner, BaseUser, HostingPartner
from base_app.services import send_activation_mail, send_forgotten_password_email
from base_app.helper import get_or_none

from .forms import RegisterForm, LoginForm
from .decorators import anonymous_required


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
    hosting_partners = HostingPartner.objects.all().order_by('?')
    hosting_partners = [gp.partner for gp in hosting_partners]
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
    form = RegisterForm()
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


@login_required
def profile(request):
    return render(request, 'website/profile.html', locals())


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
