from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = 'base.html'


class ChooseInterviewView(TemplateView):
    template_name = 'choose_interview.html'
