from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from loki.applications.models import Application
from .models import Interview
# Create your views here.


class ChooseInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'choose_interview.html'

    def dispatch(self, request, *args, **kwargs):
        self.interview = Interview.objects.get(has_confirmed=True)
        if self.interview:
            return HttpResponseRedirect('confirm')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['interviews'] = Interview.objects.filter(application__isnull=True)

        return context


class ConfirmInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_interview.html'

    def dispatch(self, request, *args, **kwargs):
        self.application = Application.objects.filter(user=self.request.user).filter(
                                                 has_interview_date=True).first()
        self.interview = Interview.objects.get(application=self.application)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['application'] = self.application
        context['interview'] = self.interview

        return context

    def post(self, request, *args, **kwargs):
        self.interview.has_confirmed = True
        self.interview.save()

        return super().get(request, *args, **kwargs)
