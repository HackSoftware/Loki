from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from djoser import views

from .serializers import CompetitorSerializer
from .permissions import IsHackFMIUser


class Login(views.LoginView):

    def action(self, serializer):
        response = super(Login, self).action(serializer)
        user = serializer.object
        if not user.get_competitor():
            response.status_code = 206
        return response


@api_view(['GET'])
@permission_classes((IsHackFMIUser,))
def me(request):
    logged_competitor = request.user.get_competitor()
    serializer = CompetitorSerializer(logged_competitor, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
