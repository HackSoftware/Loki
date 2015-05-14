from django.conf.urls import url

from .views import email_form_view, home_page


urlpatterns = [
    url(r'^email_form/$', email_form_view, name='email_form'),
    url(r'^$', home_page, name='home'),
]
