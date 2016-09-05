from django.conf.urls import url

from djoser.views import LoginView
from .views import (me, baseuser_update, base_user_update,
                    education_place_suggest,
                    user_activation, user_password_reset)


urlpatterns = [
    url(r'^user-activation/(?P<token>[\w-]+)$', user_activation, name="user_activation"),
    url(r'^user-password-reset/(?P<token>[\w-]+)$', user_password_reset,
        name="user_password_reset"),
    url(r'^api/login/', LoginView.as_view(), name='login'),
    url(r'^api/me/$', me, name='me'),
    url(r'^api/baseuser-update', baseuser_update, name='update_baseuser'),
    url(r'^api/base-user-update/$', base_user_update, name='base_user_update'),
    url(r'^api/education-place-suggest/$', education_place_suggest,
        name='education_place_suggest'),
]
