from django.conf.urls import url

from .views import apply_overview, apply_course, edit_application, edit_applications

urlpatterns = [
    url(r'^edit/$', edit_applications, name="edit_applications"),
    url(r'^$', apply_overview, name="apply_overview"),
    url(r'^(?P<course_url>[-\w]+)/$', apply_course, name="apply_course"),
    url(r'^edit/(?P<course_url>[-\w]+)$', edit_application, name="edit_application")
]
