from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Language
from .serializers import LanguageSerializer


class LanguageListView(APIView):
    def get(self, request, format=None):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
