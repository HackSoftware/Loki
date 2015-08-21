from django.conf.urls import url

from .views import index, about

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about$', about, name="about")
]
