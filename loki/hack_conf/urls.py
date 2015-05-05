from django.conf.urls import url

from .views import email_form_view


urlpatterns = [
    url(r'^', email_form_view, name='email_form'),
]