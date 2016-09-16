from django.views.generic import TemplateView

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html", locals())

class IndexView(TemplateView):
    template_name = 'base.html'

class ChooseInterviewView(TemplateView):
    template_name = 'choose_interview.html'
