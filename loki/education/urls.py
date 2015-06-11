from django.conf.urls import url
from education.views import (set_check_in, get_lectures, get_check_ins,
                             get_courses, OnBoardStudent, student_update)


urlpatterns = [
    url(r'^set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^get-lectures/$', get_lectures, name='get_lectures'),
    url(r'^get-check-ins/$', get_check_ins, name='get_check_ins'),
    url(r'^get-courses/$', get_courses, name='get_courses'),
    url(r'^api/student-update/$', student_update, name='student_update'),
    url(r'^api/onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
]
