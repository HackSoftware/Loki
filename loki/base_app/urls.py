from django.conf.urls import url

from .views import user_activation, user_password_reset


urlpatterns = [
    url(r'^user-activation/(?P<token>[\w-]+)$', user_activation, name="user_activation"),
    url(r'^user-password-reset/(?P<token>[\w-]+)$', user_password_reset,
        name="user_password_reset"),
]
