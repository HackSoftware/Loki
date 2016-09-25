from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from loki.applications.models import Application
from .models import Interview
# Create your views here.


class ChooseInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'choose_interview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['interviews'] = Interview.objects.filter(application__isnull=True)

        return context


class ConfirmInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_interview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        print(user)
        context['application'] = Application.objects.filter(user=user).filter(has_interview_date=True).first()
        context['interview'] = Interview.objects.get(application=context['application'])

        return context
