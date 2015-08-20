import json
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from base_app.models import Event, Ticket

from base_app.serializers import (BaseUserMeSerializer, UpdateBaseUserSerializer, EventSerializer, TicketSerializer)
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


# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def buy_ticket(request):
#     event_id = request.data.get('event_id')
#     user = request.user
#     event = get_object_or_404(Event, id=event_id)

#     try:
#         ticket = Ticket(event=event, base_user=user)
#         ticket.save()
#     except ValidationError:
#         error = {"error": "Вече си си закупил билет. Имаш право само на един билет."}
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)
#     return Response(status=status.HTTP_201_CREATED)


class TicketAPI(generics.CreateAPIView):
    model = Ticket
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        serializer.save(base_user=self.request.user)


@api_view(['GET'])
def get_number_of_sold_tickets(request):
    count = Ticket.objects.count()
    return Response({'item': [{"value": count}]}, status=status.HTTP_200_OK)


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
