from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = 'base.html'


class ChooseInterviewView(TemplateView):
    template_name = 'choose_interview.html'

class ConfirmInterviewView(TemplateView):
    template_name = 'confirm_interview.html'
