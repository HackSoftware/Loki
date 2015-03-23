from django.conf.urls import url
from .views import LanguageListView


urlpatterns = [
    url(r'^api/languages/$', LanguageListView.as_view(), name='languages'),
]
