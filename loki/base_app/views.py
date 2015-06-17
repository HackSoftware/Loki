from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from base_app.models import Event, Ticket

from base_app.serializers import BaseUserMeSerializer, UpdateBaseUserSerializer, EventSerializer


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
    serializer = UpdateBaseUserSerializer(baseuser, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def buy_ticket(request):
    event_id = request.data.get('event_id')
    user = request.user
    event = get_object_or_404(Event, id=event_id)

    try:
        ticket = Ticket(event=event, base_user=user)
        ticket.save()
    except ValidationError:
        error = {"error": "Вече си си закупил билет. Имаш право само на един билет."}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_number_of_sold_tickets(request):
    count = Ticket.objects.count()
    return Response({'item': [{"value": count}]}, status=status.HTTP_200_OK)
