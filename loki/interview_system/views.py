from django.views.generic import TemplateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from loki.applications.models import Application
from .models import Interview
# Create your views here.


class ChooseInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'choose_interview.html'

    def dispatch(self, request, *args, **kwargs):

        application_id = kwargs.get('application')
        self.application = Application.objects.filter(id=application_id).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['interviews'] = Interview.objects.filter(
                                application__isnull=True).order_by('date', 'start_time')

        return context

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('interview_token')
        new_interview = Interview.objects.filter(uuid=uuid).first()
        old_interview = Interview.objects.filter(application=self.application).first()
        old_interview.application = None
        old_interview.save()
        new_interview.application = self.application
        new_interview.save()


        return super().get(request, *args, **kwargs)


class ConfirmInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_interview.html'


    def dispatch(self, request, *args, **kwargs):

        uuid = kwargs.get('interview_token')
        app_id = kwargs.get('application')
        self.interview = Interview.objects.filter(uuid=uuid).first()
        print(self.interview.application.id != app_id)
        print(type(self.interview.application.id))
        print(type(app_id))
        print(self.interview.application.user != request.user)
        if self.interview.application.user != request.user or \
                self.interview.application.id != int(app_id):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interview'] = self.interview

        return context

    def post(self, request, *args, **kwargs):
        self.interview.has_confirmed = True
        self.interview.save()

        return super().get(request, *args, **kwargs)
