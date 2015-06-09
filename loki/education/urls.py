from django.conf.urls import url

from .views import set_check_in, OnBoardStudent, student_update


urlpatterns = [
    url(r'^api/set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^api/student-update/$', student_update, name='student_update'),
    url(r'^api/onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
]
