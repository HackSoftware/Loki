from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from loki.base_app.models import (
    Partner,
    GeneralPartner,
    BaseUser
)
from loki.base_app.services import (
    send_activation_mail,
    send_forgotten_password_email
)
from loki.base_app.helper import get_or_none

from loki.education.models import (
    WorkingAt,
    Student,
    Teacher
)
from loki.education.helper import check_macs_for_student

from loki.applications.models import ApplicationInfo

from loki.interview_system.models import Interview

from .models import (
    SuccessVideo,
    SuccessStoryPerson,
    Course,
    CourseDescription
)
from .forms import (
    RegisterForm,
    LoginForm,
    BaseEditForm,
    StudentEditForm,
    TeacherEditForm
)
from .mixins import SnippetBasedView, AnonymousRequired


class IndexView(SnippetBasedView, TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['successors'] = SuccessStoryPerson.objects.filter(show_picture_on_site=True).order_by('?')[:6]
        context['partners'] = Partner.objects.all().order_by('?')
        context['videos'] = SuccessVideo.objects.all()[:4]

        context['success'] = WorkingAt.objects.filter(came_working=False)
        context['success_students'] = map(lambda x: x.student, context['success'])
        context['success_students_count'] = len(set(context['success_students']))

        return context


class AboutView(SnippetBasedView, TemplateView):
    template_name = 'website/about.html'


class CoursesView(SnippetBasedView, TemplateView):
    template_name = 'website/courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['opened_course_applications'] = ApplicationInfo.objects.get_open_for_apply()
        context['active_courses'] = Course.objects.get_active_courses()
        context['closed_courses_without_cd'] = Course.objects\
                                                     .get_closed_courses()\
                                                     .filter(coursedescription__isnull=False)\
                                                     .order_by('-start_time')

        return context


class PartnersView(SnippetBasedView, TemplateView):
    template_name = 'website/partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        general_partners = GeneralPartner.objects.all().order_by('?')
        context['general_partners'] = [gp.partner for gp in general_partners]
        context['partners'] = Partner.objects.all().order_by('?')

        return context


class CourseDetailsView(SnippetBasedView, TemplateView):
    template_name = 'website/course_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cd = get_object_or_404(CourseDescription, url=self.kwargs['course_url'])

        context['cd'] = cd
        context['teachers'] = cd.course.teacher_set.all()
        context['partners'] = cd.course.partner.all().order_by('?')
        context['course_days'] = ' '.join([word.strip() for word in cd.course_days.split(',')])

        return context


class RegisterView(AnonymousRequired, FormView):
    template_name = 'website/auth/register.html'
    form_class = RegisterForm

    def dispatch(self, *args, **kwargs):
        self.origin = self.request.GET.get('origin', None)

        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        return {'origin': self.origin}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['origin'] = self.origin

        return context

    def form_valid(self, form):
        user = form.save()
        send_activation_mail(self.request, user)

        return render(self.request, 'website/auth/thanks.html')


class LogInView(AnonymousRequired, FormView):
    template_name = 'website/auth/login.html'
    form_class = LoginForm

    def dispatch(self, *args, **kwargs):
        self.error = None

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        url = self.request.GET.get('next', reverse('website:profile'))
        return url

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            self.error = "Невалидни email и/или парола"
            return self.form_invalid(form)

        if not user.is_active:
            self.error = "Моля активирай акаунта си"
            return self.form_invalid(form)

        login(self.request, user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['error'] = self.error

        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('website:index'))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'website/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user

        try:
            student = Student.objects.get(email=self.request.user.email)
        except Student.DoesNotExist:
            student = None
        finally:
            context['student'] = student

        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            teacher = None
        finally:
            context['teacher'] = teacher

        context['interviews'] = Interview.objects.get_active(self.request.user)

        return context


class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'website/profile_edit.html'
    form_class = BaseEditForm
    success_url = reverse_lazy('website:profile_edit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


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
            check_macs_for_student(student, student.mac)
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
            check_macs_for_student(teacher, teacher.mac)
            if Student.objects.filter(email=request.user.email).exists():
                student = Student.objects.get(email=request.user.email)
                StudentEditForm(request.POST, request.FILES,
                                instance=student).save()
        else:
            errors = teacher_form.errors
            return render(request, "website/profile_edit_teacher.html", locals())
    return render(request, 'website/profile_edit_teacher.html', locals())


class ForgottenPasswordView(TemplateView):
    """
    REFACTOR: Make this a FormView
    We are using a plain html form in the template. Can be done better.
    """
    template_name = 'website/auth/forgotten_password.html'

    def dispatch(self, *args, **kwargs):
        self.message = None

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['message'] = self.message

        return context

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email', '').strip()
        baseuser = get_or_none(BaseUser, email=email)
        if baseuser is None:
            self.message = "Потребител с посочения email не е открит"
        else:
            self.message = "Email за промяна на паролата беше изпратен на посочения адрес"
            send_forgotten_password_email(self.request, baseuser)

        return self.get(*args, **kwargs)
