from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base_app.serializers import BaseUserMeSerializer, UpdateBaseUserSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def me(request):
    logged_user = request.user
    serializer = BaseUserMeSerializer(logged_user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def baseuser_update(request):
    student = request.user.get_student()
    serializer = UpdateBaseUserSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)
