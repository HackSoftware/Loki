from django.conf.urls import url
from .views import LanguageListView, register, Login

urlpatterns = [
    url(r'^api/languages/$', LanguageListView.as_view(), name='languages'),
    url(r'^api/register/$', register, name='register'),
    url(r'^api/login/', Login.as_view(), name='login')
]
