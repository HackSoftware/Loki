from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework_jwt.views import ObtainJSONWebToken

from .models import Skill

from .serializers import SkillSerializer, CompetitorSerializer


class SkillListView(APIView):
    def get(self, request, format=None):
        languages = Skill.objects.all()
        serializer = SkillSerializer(languages, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CompetitorSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(serializer._validated_data['password'])
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainJSONWebToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user')
            if not user.get_competitor():
                return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)

        return super(Login, self).post(request)
