from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from djoser import views

from .serializers import CompetitorSerializer
from .premissions import IsHackFMIUser


class Login(views.LoginView):

    def action(self, serializer):
        response = super(Login, self).action(serializer)
        user = serializer.object
        if not user.get_competitor():
            response.status = status.HTTP_206_PARTIAL_CONTENT

        return response


@api_view(['GET'])
@permission_classes((IsHackFMIUser,))
def me(request):
    logged_competitor = request.user.get_competitor()
    serializer = CompetitorSerializer(logged_competitor, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
