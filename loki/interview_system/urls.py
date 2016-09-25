from django.conf.urls import url

# from .views import (index, get_students, get_emails, get_all_emails, confirm_interview,
#                     choose_interview, confirm_slot, get_interview_slots, confirm_student_interview)

from .views import ChooseInterviewView, ConfirmInterviewView


urlpatterns = [
    url(r'^choose_interview$', ChooseInterviewView.as_view(), name='choose_interview'),
    url(r'^confirm_interview$', ConfirmInterviewView.as_view(), name='confirm_interview')
]
