from django.conf.urls import url
from djoser.views import ActivationView, PasswordResetConfirmView

from base_app.auth import RegistrationView, Login, PasswordResetView
from base_app.views import me, baseuser_update


urlpatterns = [
    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/password-reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^api/password-reset-confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^api/me/$', me, name='me'),
    url(r'^api/update-baseuser', baseuser_update, name='update_baseuser')
]
