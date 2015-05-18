from django.conf.urls import patterns, include, url
from education.views import set_check_in


urlpatterns = patterns(
    url(r'^set-check-in/$', set_check_in, name='set_check_in'),
)
