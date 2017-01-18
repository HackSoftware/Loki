from django.conf.urls import url

from .views import (
    IndexView,
    AboutView,
    CoursesView,
    PartnersView,
    CourseDetailsView,
    RegisterView,
    LogInView,
    ProfileView,
    ProfileEditView,
    StudentProfileEditView,
    TeacherProfileEditView,
    ForgottenPasswordView,
    logout_view
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^courses/$', CoursesView.as_view(), name='courses'),
    url(r'^partners/$', PartnersView.as_view(), name='partners'),
    url(r'^courses/(?P<course_url>[-\w]+)/$', CourseDetailsView.as_view(), name='course_details'),
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', ProfileEditView.as_view(), name='profile_edit'),
    url(r'^profile/edit/student$', StudentProfileEditView.as_view(),
        name='profile_edit_student'),
    url(r'^profile/edit/teacher$', TeacherProfileEditView.as_view(), name='profile_edit_teacher'),
    url(r'^forgotten-password/$', ForgottenPasswordView.as_view(), name='forgotten_password'),
]
