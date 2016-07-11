from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from post_office import mail

from .models import (Skill, Competitor, Team, TeamMembership,
                     Mentor, Season, TeamMentorship)
from .serializers import (SkillSerializer, TeamSerializer, Invitation,
                          InvitationSerializer, MentorSerializer,
                          SeasonSerializer, PublicTeamSerializer,
                          OnBoardingCompetitorSerializer,
                          TeamMembershipSerializer,
                          TeamMentorshipSerializer,
                          )
from .permissions import (IsHackFMIUser, IsTeamLeaderOrReadOnly,
                          IsMemberOfTeam, IsTeamMembershipInActiveSeason,
                          IsTeamLeader, IsSeasonDeadlineUpToDate,
                          IsMentorDatePickUpToDate,
                          IsTeamInActiveSeason, CanInviteMoreMembers,
                          IsTeamleaderOrCantCreate,
                          # IsInvitationSentToInvitedMember,
                          IsInvitedMemberAlreadyInYourTeam,
                          IsInvitedMemberAlreadyInOtherTeam,
                          CanDeleteInvitation)
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
    permission_classes = (IsHackFMIUser, IsTeamLeaderOrReadOnly,
                          IsSeasonDeadlineUpToDate, IsTeamInActiveSeason)
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.all()

    def perform_create(self, serializer):
        season = Season.objects.get(is_active=True)
        team = serializer.save()
        team.season = season
        team.add_member(self.request.user.get_competitor(), is_leader=True)
        team.save()


class TeamMembershipAPI(generics.DestroyAPIView):
    permission_classes = (IsHackFMIUser, IsMemberOfTeam,
                          IsTeamMembershipInActiveSeason,)

    serializer_class = TeamMembershipSerializer

    def get_queryset(self):
        return TeamMembership.objects.all()

    def perform_destroy(self, instance):
        # Remove team if teamleader leaves
        if instance.is_leader is True:
            team = instance.team
            send_team_delete_email(team)
            team.delete()
        instance.delete()


class TeamMentorshipAPI(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    permission_classes = (IsHackFMIUser, IsTeamLeader,
                          IsMentorDatePickUpToDate)

    serializer_class = TeamMentorshipSerializer
    queryset = TeamMentorship.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InvitationView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):

    permission_classes = (IsHackFMIUser, IsTeamleaderOrCantCreate,
                          IsInvitedMemberAlreadyInYourTeam,
                          IsInvitedMemberAlreadyInOtherTeam,
                          CanInviteMoreMembers,
                          CanDeleteInvitation,)

    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(competitor=self.request.user,
                                         team__season__is_active=True)

    def get_object(self):
        obj = Invitation.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        team = TeamMembership.objects.get(competitor=self.request.user, team__season__is_active=True).team

        #TODO: signals for email sending
        # sender = settings.DEFAULT_FROM_EMAIL
        # mail.send(
        #     competitor.email,
        #     sender,
        #     template='hackfmi_team_invite',
        # )

        serializer.save(team=team)

    def perform_destroy(self, instance):

            # Remove team if teamleader leaves

        if instance.team.get_leader():
            membership = TeamMembership.objects.filter(team=instance.team,
                                                       competitor=instance.competitor)
            membership.delete()
        instance.delete()


@api_view(['GET'])
def get_schedule(request):
    content = ""

    with open("media/mentors.html", "r") as f:
        content = f.read()

    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((AllowAny, ))
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
