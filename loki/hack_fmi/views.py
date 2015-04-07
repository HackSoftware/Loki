from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Skill, Competitor, Team, TeamMembership, Mentor
from .serializers import (SkillSerializer, TeamSerializer,
                          Invitation, InvitationSerializer, MentorSerializer)

from .premissions import IsHackFMIUser


class SkillListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class TeamAPI(generics.ListCreateAPIView):
    permission_classes = (IsHackFMIUser,)
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        needed_id = self.request.QUERY_PARAMS.get('id', None)
        if needed_id is not None:
            queryset = queryset.filter(id=needed_id)
        return queryset

    def perform_create(self, serializer):
        team = serializer.save()
        team.add_member(self.request.user.get_competitor(), is_leader=True)


@api_view(['POST'])
@permission_classes((IsHackFMIUser,))
def leave_team(request):
    logged_competitor = request.user.get_competitor()
    membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
    team = Team.objects.get(id=membership.team.id)
    if membership.is_leader:
        members = list(team.members.all())
        user_emails = [member.email for member in members]

        send_mail(
            'Изтрит отбор HackFMI',
            'Лидера на твоя отбор напусна и отбора беше изтрит.',
            'register@hackfmi.com',
            user_emails,
            fail_silently=False
        )
        team.delete()
        return Response(status=status.HTTP_200_OK)
    TeamMembership.objects.get(competitor=logged_competitor).delete()
    return Response(status=status.HTTP_200_OK)


class InvitationView(APIView):
    permission_classes = (IsHackFMIUser,)

    def post(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
        invited_competitor = Competitor.objects.filter(email=request.data['email']).first()
        if not invited_competitor:
            error = {"error": "Този потребител все още не е регистриран в системата."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
        if Invitation.objects.filter(team=membership.team, competitor=invited_competitor).first():
            error = {"error": "Вече си изпратил покана на този участник. Изчакай да потвърди!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if membership.team in invited_competitor.team_set.all():
            error = {"error": "Този участник вече е в отбора ти!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if len(membership.team.teammembership_set.all()) >= 6:
            error = {"error": "В този отбор вече има повече от 6 човека. "
                              "Трябва някой да напусне отбора за да можеш да приемш тази покана!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if membership.is_leader:
            Invitation.objects.create(team=membership.team, competitor=invited_competitor)
            message = {"message": "Успешно изпратихте поканата за включване в отбора!"}
            return Response(message, status=status.HTTP_201_CREATED)
        message = {"message": "Трябва да бъдете лидер, за да каните хора!"}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitations = Invitation.objects.filter(competitor=logged_competitor)
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitation = Invitation.objects.get(id=request.data['id'])
        if invitation.competitor != logged_competitor:
            error = {"error": "Тази покана не е за теб."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
        if logged_competitor.team_set.all():
            error = {"error": "Вече имаш отбор. Напусни го и тогава можеш да приемеш нова покана."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        TeamMembership.objects.create(competitor=logged_competitor, team=invitation.team)
        invitation.delete()
        message = {"message": "Успешно се присъединихте към отбора."}
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitation = Invitation.objects.get(id=request.data['id'])
        if invitation.competitor != logged_competitor:
            error = {"error": "Тази покана не е за теб."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
        invitation.delete()
        return Response(status=status.HTTP_200_OK)


class MentorListView(generics.ListAPIView):
    permission_classes = (IsHackFMIUser,)
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
