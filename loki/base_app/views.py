import json
from rest_framework import status, mixins
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from base_app.models import Event, Ticket

from base_app.serializers import (BaseUserMeSerializer, UpdateBaseUserSerializer,
                                  EventSerializer, TicketSerializer)
from hack_fmi.models import BaseUser

from .helper import crop_image


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def me(request):
    logged_user = request.user
    serializer = BaseUserMeSerializer(logged_user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def baseuser_update(request):
    baseuser = request.user
    serializer = UpdateBaseUserSerializer(
        baseuser,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


class EventAPI(generics.ListAPIView):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TicketAPI(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    model = Ticket
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(base_user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(base_user=user)


@api_view(['GET'])
def get_number_of_sold_tickets(request):
    users = BaseUser.objects.filter(ticket__isnull=False)
    return Response({'item': [{"value": users.count()}]}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def base_user_update(request):
    user = request.user
    co = request.data['selection']
    co = json.loads(co)

    data = {'full_image': request.data['file']}
    serializer = UpdateBaseUserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        name = crop_image(int(co[0]), int(co[1]), int(co[3]), int(co[2]), str(user.full_image))
        user.avatar = name
        user.save()
        return Response(name, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)
