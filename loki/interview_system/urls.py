from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from .views import (ChooseInterviewView, ConfirmInterviewView,
                    GenerateInterviews)


urlpatterns = [
    url(r'^choose/(?P<application>[0-9]+)/(?P<interview_token>[-\w]+)/$',
                 ChooseInterviewView.as_view(), name='choose_interview'),
    url(r'^confirm/(?P<application>[0-9]+)/(?P<interview_token>[-\w]+)/$',
                ConfirmInterviewView.as_view(), name='confirm_interview'),
    url(r'^generate-interviews/',
                GenerateInterviews.as_view(), name='generate_interviews')
]
