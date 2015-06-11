from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hackfmi/', include('hack_fmi.urls', namespace='hack_fmi')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^hackconf/', include('hack_conf.urls')),
    url(r'^education/', include('education.urls', namespace='education')),
    url(r'^base/', include('base_app.urls', namespace='base_app')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
