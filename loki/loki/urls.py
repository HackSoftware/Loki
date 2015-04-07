from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hackfmi/', include('hack_fmi.urls', namespace='hack_fmi')),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
