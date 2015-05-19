from django.conf.urls import patterns, url
from education.views import set_check_in


urlpatterns = [
    url(r'^set-check-in/$', set_check_in, name='set_check_in'),
]
