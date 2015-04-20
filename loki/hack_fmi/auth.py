from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from djoser import views
from post_office import mail

from .serializers import CompetitorSerializer
from .premissions import IsHackFMIUser


class RegistrationView(views.RegistrationView):

    def send_email(self, to_email, from_email, context):
        mail.send(
            to_email,
            from_email,
            template='user_register',
            context=context,
        )

    def get_serializer_class(self):
        return CompetitorSerializer


class PasswordResetView(views.PasswordResetView):
    def get_send_email_extras(self):
        return {
            'subject_template_name': settings.BASE_DIR + '/hack_fmi/templates/password_reset_email_subject.txt',
            'plain_body_template_name': settings.BASE_DIR + '/hack_fmi/templates/password_reset_email_body.txt',
        }


class Login(views.LoginView):
    def action(self, serializer):
        user = serializer.object
        if not user.get_competitor():
            return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)
        return super(Login, self).action(serializer)


@api_view(['GET'])
@permission_classes((IsHackFMIUser,))
def me(request):
    logged_competitor = request.user.get_competitor()
    serializer = CompetitorSerializer(logged_competitor, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
