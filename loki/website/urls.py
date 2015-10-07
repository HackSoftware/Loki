from django.conf.urls import url

from .views import index, about, courses, partners, course_details

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name="about"),
    url(r'^courses/$', courses, name="courses"),
    url(r'^partners/$', partners, name="partners"),
    url(r'^courses/(?P<course_url>[a-z0-9-]+)$', course_details, name="course_details")
]
