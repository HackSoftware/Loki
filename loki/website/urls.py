from django.conf.urls import url

from .views import (index, about, courses, partners, course_details, register,
                    log_in, profile, profile_edit, profile_edit_teacher,
                    profile_edit_student, forgotten_password, logout_view,
                    apply_overview, apply_course)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name="about"),
    url(r'^courses/$', courses, name="courses"),
    url(r'^partners/$', partners, name="partners"),
    url(r'^courses/(?P<course_url>[-\w]+)/$', course_details,
        name="course_details"),
    url(r'^login/$', log_in, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', register, name="register"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^profile/edit/$', profile_edit, name="profile_edit"),
    url(r'^profile/edit/student$', profile_edit_student,
        name="profile_edit_student"),
    url(r'^profile/edit/teacher$', profile_edit_teacher,
        name="profile_edit_teacher"),
    url(r'^forgotten-password/$', forgotten_password, name="forgotten_password"),
    url(r'^apply/$', apply_overview, name="apply_overview"),
    url(r'^apply/(?P<course_url>[-\w]+)/$', apply_course, name="apply_course")
]
