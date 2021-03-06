from django.views.generic import TemplateView, FormView, CreateView
from django.views.generic.base import View
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

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
    TeacherEditForm,
    WorkingAtForm
)
from .mixins import (
    AddSnippetsToContext,
    AddUserToContext,
    AnonymousRequired,
    CanAccessWorkingAtPermissionMixin
)


class IndexView(AddSnippetsToContext, TemplateView):
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


class CorporateTrainingsView(AddSnippetsToContext, TemplateView):
    template_name = 'website/corporate_trainings.html'


class AboutView(AddSnippetsToContext, TemplateView):
    template_name = 'website/about.html'


class CoursesView(AddSnippetsToContext, TemplateView):
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


class PartnersView(AddSnippetsToContext, TemplateView):
    template_name = 'website/partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        general_partners = GeneralPartner.objects.all().order_by('?')
        context['general_partners'] = [gp.partner for gp in general_partners]
        context['partners'] = Partner.objects.all().order_by('?')

        return context


class CourseDetailsView(AddSnippetsToContext, TemplateView):
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

        context['RECAPTCHA_SITE_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
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


class ProfileView(LoginRequiredMixin, AddUserToContext, TemplateView):
    template_name = 'website/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            student = Student.objects.get(email=self.request.user.email)
            context['jobs'] = WorkingAt.objects.filter(student=student).order_by('start_date').all()
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


class ProfileEditView(LoginRequiredMixin, AddUserToContext, FormView):
    template_name = 'website/profile_edit.html'
    form_class = BaseEditForm
    success_url = reverse_lazy('website:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


class StudentProfileEditView(LoginRequiredMixin, AddUserToContext, FormView):
    template_name = 'website/profile_edit_student.html'
    success_url = reverse_lazy('website:profile')
    form_class = StudentEditForm

    def dispatch(self, *args, **kwargs):
        self.student = get_or_none(Student, email=self.request.user.email)

        if self.student is None:
            return redirect(reverse('website:profile'))

        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['instance'] = self.student

        return kwargs

    def form_valid(self, form):
        form.save()
        check_macs_for_student(self.student, self.student.mac)

        if Teacher.objects.filter(email=self.request.user.email).exists():
            teacher = Teacher.objects.get(email=self.request.user.email)
            TeacherEditForm(self.request.POST, self.request.FILES,
                            instance=teacher).save()

        return super().form_valid(form)


class TeacherProfileEditView(LoginRequiredMixin, AddUserToContext, FormView):
    template_name = 'website/profile_edit_teacher.html'
    success_url = reverse_lazy('website:profile')
    form_class = TeacherEditForm

    def dispatch(self, *args, **kwargs):
        self.teacher = get_or_none(Teacher, email=self.request.user.email)

        if self.teacher is None:
            return redirect(reverse('website:profile'))

        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['instance'] = self.teacher

        return kwargs

    def form_valid(self, form):
        form.save()
        check_macs_for_student(self.teacher, self.teacher.mac)

        if Student.objects.filter(email=self.request.user.email).exists():
            student = Student.objects.get(email=self.request.user.email)
            StudentEditForm(self.request.POST, self.request.FILES,
                            instance=student).save()

        return super().form_valid(form)


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


class WorkingAtCreateView(LoginRequiredMixin,
                          CanAccessWorkingAtPermissionMixin,
                          CreateView):
    model = WorkingAt
    form_class = WorkingAtForm
    success_url = reverse_lazy('website:profile')

    def form_valid(self, form):
        student = self.request.user.get_student()
        working_at = form.save(commit=False)
        working_at.student = student
        working_at.save()

        student.looking_for_job = form.cleaned_data.get('looking_for_job', False)
        student.save()

        return super().form_valid(form)


class StudentLookingForJobUpdateView(LoginRequiredMixin,
                                     CanAccessWorkingAtPermissionMixin,
                                     View):

    def post(self, request, *args, **kwargs):
        student = self.request.user.get_student()
        student.looking_for_job = True
        student.save()
        return redirect(reverse_lazy('website:profile'))
