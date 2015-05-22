from django.conf.urls import url

from .views import set_check_in, OnBoardStudent


urlpatterns = [
    url(r'^set-check-in/$', set_check_in, name='set_check_in'),

    url(r'^onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
]
