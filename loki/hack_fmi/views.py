from datetime import date
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from post_office import mail

from .models import Skill, Competitor, Team, TeamMembership, Mentor, Season
from .serializers import (SkillSerializer, TeamSerializer,
                          Invitation, InvitationSerializer, MentorSerializer, SeasonSerializer, PublicTeamSerializer, OnBoardingCompetitorSerializer)
from .premissions import IsHackFMIUser, IsTeamLeaderOrReadOnly
from .helper import send_team_delete_email


from base_app.helper import try_open
import json


class SkillListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class MentorListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Mentor.objects.filter(seasons__is_active=True)
    serializer_class = MentorSerializer


class SeasonListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Season.objects.filter(is_active=True)
    serializer_class = SeasonSerializer


class PublicTeamView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Team.objects.filter(season__is_active=True)
    serializer_class = PublicTeamSerializer


class TeamAPI(generics.UpdateAPIView, generics.ListCreateAPIView):
    permission_classes = (IsHackFMIUser, IsTeamLeaderOrReadOnly)
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.filter(season__is_active=True)
        # TODO: Use django filters
        needed_id = self.kwargs.get('pk', None)
        if needed_id:
            queryset = queryset.filter(pk=needed_id)
        return queryset

    def perform_create(self, serializer):
        season = Season.objects.get(is_active=True)
        if season.make_team_dead_line < date.today():
            raise PermissionDenied("You are pass the deadline for creating teams!")
        team = serializer.save()
        team.season = season
        team.add_member(self.request.user.get_competitor(), is_leader=True)
        team.save()


@api_view(['POST'])
@permission_classes((IsHackFMIUser,))
def leave_team(request):
    logged_competitor = request.user.get_competitor()
    logged_competitor_teams = logged_competitor.team_set
    current_season = Season.objects.get(is_active=True)
    team = logged_competitor_teams.get(season=current_season)

    if team.get_leader() == logged_competitor:
        send_team_delete_email(team)
        team.delete()
        return Response(status=status.HTTP_200_OK)

    TeamMembership.objects.get(
        competitor=logged_competitor,
        team=team
    ).delete()
    return Response(status=status.HTTP_200_OK)


class InvitationView(APIView):
    permission_classes = (IsHackFMIUser,)

    def post(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        current_season = Season.objects.get(is_active=True)
        membership = TeamMembership.objects.get(competitor=logged_competitor, team__season=current_season)
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

        if len(membership.team.teammembership_set.all()) >= current_season.max_team_members_count:
            error = {"error": "В този отбор вече има повече от 6 човека. "
                              "Трябва някой да напусне отбора за да можеш да приемш тази покана!"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        if membership.is_leader:
            Invitation.objects.create(team=membership.team, competitor=invited_competitor)
            message = {"message": "Успешно изпратихте поканата за включване в отбора!"}
            sender = settings.DEFAULT_FROM_EMAIL
            mail.send(
                invited_competitor.email,
                sender,
                template='hackfmi_team_invite',
            )
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
        current_season = Season.objects.get(is_active=True)
        if invitation.competitor != logged_competitor:
            error = {"error": "Тази покана не е за теб."}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
        if logged_competitor.team_set.filter(season=current_season):
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


class AssignMentor(APIView):
    permission_classes = (IsHackFMIUser,)

    def put(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        mentor = Mentor.objects.get(id=request.data['id'])
        season = Season.objects.get(is_active=True)
        team = Team.objects.get(id=request.data['team_id'])

        today = date.today()
        if season.mentor_pick_start_date > today or season.mentor_pick_end_date < today:
            error = {"error": "В момента не може да избирате ментор."}
            return Response(error, status.HTTP_403_FORBIDDEN)

        if len(team.mentors.all()) >= season.max_mentor_pick:
            error = {"error": "Този отбор не може да има повече ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)

        if not team.get_leader() == logged_competitor:
            error = {"error": "Не си лидер на този отбор, за да избираш ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)

        team.mentors.add(mentor)
        return Response(status=status.HTTP_200_OK)

    # TODO: Fix methods
    def post(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        mentor = Mentor.objects.get(id=request.data['id'])
        team = Team.objects.get(id=request.data['team_id'])

        if not team.get_leader() == logged_competitor:
            error = {"error": "Не си лидер на този отбор, за да избираш ментори."}
            return Response(error, status.HTTP_403_FORBIDDEN)

        team.mentors.remove(mentor)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_schedule(request):
    content = ""

    with open("media/mentors.html", "r") as f:
        content = f.read()

    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def schedule_json(request):
    content = {
        "placed": {},
        "leftovers": []
    }

    with try_open("media/placing.json", "r") as (f, error):
        if error is None:
            content = json.loads(f.read())

    return Response(content, status=status.HTTP_200_OK)


class OnBoardCompetitor(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if not request.user.get_competitor():
            serializer = OnBoardingCompetitorSerializer(data=request.data, baseuser=request.user)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
