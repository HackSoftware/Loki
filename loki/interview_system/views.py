from django.db import transaction
from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from rest_framework import generics

from loki.applications.models import Application, ApplicationInfo
from .models import Interview, Interviewer
from .serializers import InterviewSerializer


class CannotConfirmOthersInterviewMixin:
    """
    TODO:
    1. Find a better place to live.
    2. Refactor it.
    """
    def dispatch(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        application_id = kwargs.get('application')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        self.application = Application.objects.filter(id=application_id).first()
        self.interviewer = Interviewer.objects.filter(interview=self.interview).first()

        if self.application.user != request.user or \
           self.application.id != int(application_id):
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class ChooseInterviewView(LoginRequiredMixin, CannotConfirmOthersInterviewMixin, TemplateView):
    template_name = 'choose_interview.html'

    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('application')

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
        uuid = kwargs.get('interview_token')
        application = kwargs.get('application')
        context['current_interview'] = Interview.objects.filter(
                                       uuid=uuid).first()
        context['app'] = Application.objects.filter(id=application).first()
        context['interviews'] = Interview.objects.free_slots_for(context['app'].application_info)

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        application_id = kwargs.get('application')
        new_interview = Interview.objects.filter(uuid=uuid).first()

        if new_interview.application is not None:
            raise Http404

        old_interview = Interview.objects.filter(application=self.application).first()
        old_interview.reset()

        new_interview.application = self.application
        new_interview.has_received_email = True
        new_interview.has_confirmed = True
        new_interview.save()

        return redirect(reverse('interview_system:confirm_interview',
                        kwargs={'application': application_id,
                                'interview_token': new_interview.uuid}))


class ConfirmInterviewView(LoginRequiredMixin, CannotConfirmOthersInterviewMixin, TemplateView):
    template_name = 'confirm_interview.html'

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
        if Interview.objects.filter(application=self.application, has_confirmed=True).exists():
            raise Http404

        self.interview.has_confirmed = True
        self.interview.save()

        return super().get(request, *args, **kwargs)


class GenerateInterviews(LoginRequiredMixin, TemplateView,):
    template_name = 'generate_interviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_infos'] = ApplicationInfo.objects.get_open_for_interview()

        confirmed_interviews = {}
        for info in context['app_infos']:
            confirmed_interviews[info] = Interview.objects.confirmed_for(info).count()
        context['confirmed_interviews'] = confirmed_interviews
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        call_command('generate_interview_slots')
        return super().get(request, *args, **kwargs)


class GetFreeInterviews(generics.ListAPIView, LoginRequiredMixin):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.get_free_slots().order_by('date', 'start_time')

    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        self.app_id = request.GET.get('applicationId')
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'user': self.user,
                'application': self.app_id}
