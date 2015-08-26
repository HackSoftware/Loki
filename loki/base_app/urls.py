from django.conf.urls import url
from djoser.views import ActivationView, PasswordResetConfirmView

from base_app.auth import RegistrationView, Login, PasswordResetView
from base_app.views import (me, baseuser_update, EventAPI, TicketAPI, get_number_of_sold_tickets,
                            base_user_update)


urlpatterns = [
    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/password-reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^api/password-reset-confirm/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^api/me/$', me, name='me'),
    url(r'^api/baseuser-update', baseuser_update, name='update_baseuser'),
    url(r'^api/event/$', EventAPI.as_view(), name='event'),
    url(r'^api/ticket/$', TicketAPI.as_view(), name='ticket'),
    url(r'^api/ticket/(?P<pk>[0-9]+)/$', TicketAPI.as_view(), name='ticket_edit'),

    url(r'^api/get_number_of_sold_tickets/$', get_number_of_sold_tickets, name='get_number_of_sold_tickets'),
    url(r'^api/base-user-update/$', base_user_update, name='base_user_update'),
]
