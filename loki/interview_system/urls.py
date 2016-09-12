from django.conf.urls import url

from .views import IndexView, ChooseInterviewView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^/choose_interview$', ChooseInterviewView.as_view(), name='choose_interview'),
]
