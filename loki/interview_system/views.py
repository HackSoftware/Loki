from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from loki.applications.models import Application
from .models import Interview, Interviewer

class ChooseInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'choose_interview.html'

    def dispatch(self, request, *args, **kwargs):

        application_id = kwargs.get('application')
        uuid = kwargs.get('interview_token')

        self.application = Application.objects.filter(id=application_id).first()

        if self.application.user != request.user or \
            self.application.id != int(application_id):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        application_id = kwargs.get('application')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        if self.interview is None or \
            self.interview.application is None or \
            self.interview.application.user != request.user or \
            self.interview.application.id != int(application_id):
            raise Http404

        if self.interview.has_confirmed:
            return redirect(reverse('interview_system:confirm_interview',
                            kwargs={'application': application_id,
                            'interview_token': self.interview.uuid}))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        uuid = kwargs.get('interview_token')
        application = kwargs.get('application')
        context['current_interview'] = Interview.objects.filter(
                                       uuid=uuid).first()
        context['interviews'] = Interview.objects.get_free_slots()

        context['app'] = Application.objects.filter(id=application).first()

        return context

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        application_id = kwargs.get('application')
        new_interview = Interview.objects.filter(uuid=uuid).first()

        if new_interview.application is not None:
            raise Http404

        old_interview = Interview.objects.filter(application=self.application).first()
        old_interview.application = None
        old_interview.save()
        new_interview.application = self.application
        new_interview.has_confirmed = True
        new_interview.save()

        return redirect(reverse('interview_system:confirm_interview',
                        kwargs={'application': application_id,
                                'interview_token': new_interview.uuid}))


class ConfirmInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_interview.html'


    def dispatch(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        app_id = kwargs.get('application')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        self.application = Application.objects.filter(id=app_id).first()
        self.interviewer = Interviewer.objects.filter(interview=self.interview).first()
        if self.application.user != request.user or \
            self.application.id != int(app_id):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interview'] = self.interview
        context['app'] = self.application
        context['interviewer'] = self.interviewer
        return context

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        application_id = kwargs.get('application')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        if self.interview is None or \
            self.interview.application is None or \
            self.interview.application.user != request.user or \
            self.interview.application.id != int(application_id):
            raise Http404

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.interview.has_confirmed = True
        self.interview.save()

        return super().get(request, *args, **kwargs)


class GenerateInterviews(LoginRequiredMixin, TemplateView):
    template_name = 'generate_interviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['free_interviews'] = Interview.objects.get_free_slots()
        context['interviews'] = Interview.objects.all()
        context['apps'] = Application.objects.all()
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        call_command('generate_interview_slots')
        return super().get(request, *args, **kwargs)
