from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ChooseInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'choose_interview.html'

class ConfirmInterviewView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_interview.html'
