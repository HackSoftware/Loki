from django.conf.urls import url

from .views import index, about, courses

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about$', about, name="about"),
    url(r'^courses$', courses, name="courses")
]
