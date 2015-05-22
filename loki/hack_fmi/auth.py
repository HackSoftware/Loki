from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from djoser import views
from post_office import mail

from .serializers import CompetitorSerializer
from .premissions import IsHackFMIUser


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
