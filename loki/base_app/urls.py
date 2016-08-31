from django.conf.urls import url
from djoser.views import ActivationView, PasswordResetConfirmView

from .auth import RegistrationView, Login, PasswordResetView
from .views import (me, baseuser_update, base_user_update,
                    education_place_suggest,
                    user_activation, user_password_reset)


urlpatterns = [
    url(r'^user-activation/(?P<token>[\w-]+)$', user_activation, name="user_activation"),
    url(r'^user-password-reset/(?P<token>[\w-]+)$', user_password_reset,
        name="user_password_reset"),
    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/password-reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^api/password-reset-confirm/$', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^api/me/$', me, name='me'),
    url(r'^api/baseuser-update', baseuser_update, name='update_baseuser'),
    url(r'^api/base-user-update/$', base_user_update, name='base_user_update'),
    url(r'^api/education-place-suggest/$', education_place_suggest,
        name='education_place_suggest'),
]
