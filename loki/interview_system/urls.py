from django.conf.urls import url

from .views import (index, get_students, get_emails, get_all_emails, confirm_interview,
                    choose_interview, confirm_slot, get_interview_slots, confirm_student_interview)

urlpatterns = [
    url(r'^$', index, name='index')
]
