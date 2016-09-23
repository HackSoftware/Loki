from django.views.generic import TemplateView

from django.shortcuts import render

# Create your views here.

class IndexView(TemplateView):
    template_name = 'base.html'

class ChooseInterviewView(TemplateView):
    template_name = 'choose_interview.html'
