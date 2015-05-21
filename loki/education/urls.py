from django.conf.urls import url
from djoser.views import ActivationView, PasswordResetConfirmView
from education.auth import RegistrationView, Login, PasswordResetView
from education.views import set_check_in


urlpatterns = [
    url(r'^set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^api/password_reset_confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
