from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Skill, Competitor, Team, TeamMembership, Mentor, Season
from .serializers import (SkillSerializer, TeamSerializer,
                          Invitation, InvitationSerializer, MentorSerializer, SeasonSerializer, PublicTeamSerializer)
from .premissions import IsHackFMIUser, IsTeamLeaderOrReadOnly
from .helper import send_team_delete_email


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
    queryset = Team.objects.all()
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
        if season.sign_up_deadline < date.today():
            raise PermissionDenied("You are pass the deadline for creating teams!")
        team = serializer.save()
        team.add_member(self.request.user.get_competitor(), is_leader=True)


@api_view(['POST'])
@permission_classes((IsHackFMIUser,))
def leave_team(request):
    logged_competitor = request.user.get_competitor()
    membership = TeamMembership.objects.get(competitor=logged_competitor)
    team = Team.objects.get(id=membership.team.id)
    if membership.is_leader:
        send_team_delete_email(team)
        team.delete()
        return Response(status=status.HTTP_200_OK)

    TeamMembership.objects.get(competitor=logged_competitor).delete()
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


@api_view(['GET'])
def get_schedule(request):
    content = ""
    with open("media/mentors.html", "r") as f:
        content = f.read()

    return Response(content, status=status.HTTP_200_OK)
