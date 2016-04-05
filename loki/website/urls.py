from django.conf.urls import url

from .views import (index, about, courses, partners, course_details, register,
                    log_in, profile, logout_view, forgotten_password)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name="about"),
    url(r'^courses/$', courses, name="courses"),
    url(r'^partners/$', partners, name="partners"),
    url(r'^courses/(?P<course_url>[-\w]+)/$', course_details, name="course_details"),
    url(r'^login/$', log_in, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register, name="register"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^forgotten-password/$', forgotten_password, name="forgotten_password")
]
