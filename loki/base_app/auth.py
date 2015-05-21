from djoser import views
from post_office import mail

from base_app.serializers import BaseUserSerializer


class RegistrationView(views.RegistrationView):

    def send_email(self, to_email, from_email, context):
        mail.send(
            to_email,
            from_email,
            template='user_register',
            context=context,
        )

    def get_serializer_class(self):
        return BaseUserSerializer


class PasswordResetView(views.PasswordResetView):

    def send_email(self, to_email, from_email, context):
        mail.send(
            to_email,
            from_email,
            template='password_reset',
            context=context,
        )


class Login(views.LoginView):

    def action(self, serializer):
        return super(Login, self).action(serializer)
