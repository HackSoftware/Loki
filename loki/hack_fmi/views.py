from datetime import date
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from post_office import mail

from .models import Skill, Competitor, Team, TeamMembership, Mentor, Season
from .serializers import (SkillSerializer, TeamSerializer,
                          Invitation, InvitationSerializer, MentorSerializer, SeasonSerializer)
from .premissions import IsHackFMIUser


class SkillListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class TeamAPI(generics.UpdateAPIView, generics.ListCreateAPIView):
    permission_classes = (IsHackFMIUser,)
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        needed_id = self.kwargs.get('pk', None)
        if needed_id:
            queryset = queryset.filter(pk=needed_id)
        return queryset

    def perform_create(self, serializer):
        season = Season.objects.filter(is_active=True).first()
        if season.sign_up_deadline < date.today():
            raise PermissionDenied("You are pass the deadline for creating teams!")
        team = serializer.save()
        team.add_member(self.request.user.get_competitor(), is_leader=True)

    def perform_update(self, serializer):
        team = self.get_object()
        if self.request.user.get_competitor() != team.get_leader():
            raise PermissionDenied("You are not a leader!")
        serializer.save()


@api_view(['POST'])
@permission_classes((IsHackFMIUser,))
def leave_team(request):
    logged_competitor = request.user.get_competitor()
    membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
    team = Team.objects.get(id=membership.team.id)
    if membership.is_leader:
        members = list(team.members.all())
        user_emails = [member.email for member in members]
        sender = settings.EMAIL_HOST_USER
        mail.send(
            user_emails,
            sender,
            template='delete_team',
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
        current_season = membership.team.season
        if not invited_competitor:
            error = {"error": "Този потребител все още не е регистриран в системата."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
        if Invitation.objects.filter(team=membership.team, competitor=invited_competitor).first():
            error = {"error": "Вече си изпратил покана на този участник. Изчакай да потвърди!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if membership.team in invited_competitor.team_set.all():
            error = {"error": "Този участник вече е в отбора ти!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if len(membership.team.teammembership_set.all()) >= current_season.max_team_members_count:
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
    permission_classes = (AllowAny,)
    queryset = Mentor.objects.filter(seasons__is_active=True)
    serializer_class = MentorSerializer


class SeasonListView(generics.ListAPIView):
    permission_classes = (IsHackFMIUser,)
    queryset = Season.objects.filter(is_active=True)
    serializer_class = SeasonSerializer


class AssignMentor(APIView):
    permission_classes = (IsHackFMIUser,)

    def put(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        mentor = Mentor.objects.get(id=request.data['id'])
        membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
        season = membership.team.season
        if season.mentor_pick_start_date > date.today() or season.mentor_pick_end_date < date.today():
            error = {"error": "В момента не може да избирате ментор."}
            return Response(error, status.HTTP_403_FORBIDDEN)
        if membership.is_leader and len(membership.team.mentors.all()) >= season.max_mentor_pick:
            error = {"error": "Този отбор не може да има повече ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)
        if membership.is_leader and len(membership.team.mentors.all()) < season.max_mentor_pick:
            membership.team.mentors.add(mentor)
            return Response(status=status.HTTP_200_OK)
        if not membership.is_leader:
            error = {"error": "Не си лидер на този отбор, за да избираш ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)

    #TODO: Fix methods
    def post(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        mentor = Mentor.objects.get(id=request.data['id'])
        membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
        if membership.is_leader:
            membership.team.mentors.remove(mentor)
            return Response(status=status.HTTP_200_OK)
        else:
            error = {"error": "Не си лидер на този отбор, за да избираш ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)
