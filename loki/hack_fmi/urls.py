from django.conf.urls import url
from .views import LanguageListView, register

urlpatterns = [
    url(r'^api/languages/$', LanguageListView.as_view(), name='languages'),
    url(r'^api/register/$', register, name='register'),
]
