from django.conf.urls import url

# from .views import (index, get_students, get_emails, get_all_emails, confirm_interview,
#                     choose_interview, confirm_slot, get_interview_slots, confirm_student_interview)

from .views import IndexView, ChooseInterviewView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^choose_interview$', ChooseInterviewView.as_view(), name='choose_interview'),
]