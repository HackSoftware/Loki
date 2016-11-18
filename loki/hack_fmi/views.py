from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import (Skill, Team, TeamMembership,
                     Mentor, Season, TeamMentorship)
from .serializers import (SkillSerializer, TeamSerializer, Invitation,
                          InvitationSerializer, MentorSerializer,
                          SeasonSerializer, PublicTeamSerializer,
                          OnBoardingCompetitorSerializer,
                          TeamMembershipSerializer,
                          TeamMentorshipSerializer,
                          CustomTeamSerializer, CompetitorSerializer)
from .permissions import (IsHackFMIUser, IsTeamLeaderOrReadOnly,
                          IsMemberOfTeam, IsTeamMembershipInActiveSeason,
                          IsTeamLeader, IsSeasonDeadlineUpToDate,
                          IsMentorDatePickUpToDate,
                          IsTeamInActiveSeason, IsTeamleaderOrCantCreateIvitation,
                          IsInvitedMemberAlreadyInYourTeam,
                          IsInvitedMemberAlreadyInOtherTeam,
                          CanInviteMoreMembersInTeam,
                          CanNotAccessWronglyDedicatedIvitation,
                          IsInvitedUserInTeam,
                          CanNotAcceptInvitationIfTeamLeader,
                          CanAttachMoreMentorsToTeam,
                          CantCreateTeamWithTeamNameThatAlreadyExists,
                          TeamLiederCantCreateOtherTeam,
                          IsInvitedMemberCompetitor)
from .helper import send_team_delete_email, send_invitation

from loki.base_app.helper import try_open

import json


class MeAPIView(generics.GenericAPIView):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsHackFMIUser, )

    def get(self, request, *args, **kwargs):
        competitor = self.request.user.get_competitor()

        # TODO: watch out if the user is not competitor
        if not competitor:
            data = {
                "is_competitor": bool(competitor),
                "competitor_info": None,
                "team": None
            }
            return Response(data=data, status=status.HTTP_200_OK)

        teams = TeamMembership.objects.list_all_teams_for_competitor(competitor=competitor)
        comp_inf = CompetitorSerializer(competitor)
        teams = CustomTeamSerializer(teams, many=True)
        data = {
            "is_competitor": bool(competitor),
            "competitor_info": comp_inf.data,
            "teams": teams.data
        }
        return Response(data=data, status=status.HTTP_200_OK)


class MeSeasonAPIView(generics.GenericAPIView):
    authentication_classes = (JSONWebTokenAuthentication, )
    # permission_classes = (IsTeamInActiveSeason, )

    def get(self, request, *args, **kwargs):
        season_id = self.kwargs.get('season_pk')
        competitor = self.request.user.get_competitor()

        # TODO: watch out if the user is not competitor
        if not competitor:
            data = {
                "is_competitor": bool(competitor),
                "competitor_info": None,
                "team": None
            }
            return Response(data=data, status=status.HTTP_200_OK)

        season = get_object_or_404(Season, pk=season_id)
        comp_inf = CompetitorSerializer(competitor)
        team_obj = Team.objects.get_all_teams_for_current_season(season=season).\
            get_all_teams_for_competitor(competitor=competitor).first()

        team = CustomTeamSerializer(team_obj)
        data = {
            "is_competitor": bool(competitor),
            "competitor_info": comp_inf.data,
            "team": team.data
        }
        return Response(data=data, status=status.HTTP_200_OK)


class SkillListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class MentorListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Mentor.objects.filter(seasons__is_active=True)
    serializer_class = MentorSerializer


class SeasonView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SeasonSerializer

    def get_object(self):
        return Season.objects.filter(is_active=True).first()


class PublicTeamView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PublicTeamSerializer
    queryset = Team.objects.filter(season__is_active=True)


class TeamAPI(mixins.CreateModelMixin,
              mixins.ListModelMixin,
              mixins.UpdateModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    permission_classes = (IsHackFMIUser, IsTeamLeaderOrReadOnly,
                          IsSeasonDeadlineUpToDate, IsTeamInActiveSeason,
                          CantCreateTeamWithTeamNameThatAlreadyExists,
                          TeamLiederCantCreateOtherTeam)
    authentication_classes = (JSONWebTokenAuthentication,)

    serializer_class = TeamSerializer
    queryset = Team.objects.all()

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
                          IsMentorDatePickUpToDate,
                          CanAttachMoreMentorsToTeam)
    authentication_classes = (JSONWebTokenAuthentication,)

    serializer_class = TeamMentorshipSerializer
    queryset = TeamMentorship.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InvitationViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.get_competitor_invitations_for_active_season(
            competitor=self.request.user.get_competitor())

    def get_object(self):
        obj = get_object_or_404(Invitation, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        # Request user is the leader of the team and he has exactly one TeamMembership.
        team = TeamMembership.objects.get_team_memberships_for_active_season(
            competitor=self.request.user.get_competitor()).first().team

        invitation = serializer.save(team=team)
        send_invitation(invitation)

    def accept(self, request, *args, **kwargs):
        invitation = self.get_object()
        TeamMembership.objects.create(team=invitation.team,
                                      competitor=invitation.competitor)
        invitation.delete()
        return Response("You have accepted this invitation!")

    @classmethod
    def get_urls(cls):
        invitation_list = cls.as_view({
            'get': 'list',
            'post': 'create',
        },
            permission_classes=[IsHackFMIUser,
                                IsTeamleaderOrCantCreateIvitation,
                                IsInvitedMemberCompetitor,
                                IsInvitedMemberAlreadyInYourTeam,
                                IsInvitedMemberAlreadyInOtherTeam,
                                CanInviteMoreMembersInTeam]
        )

        invitation_detail = cls.as_view({
            'delete': 'destroy',
        },
            permission_classes=[IsHackFMIUser,
                                CanNotAccessWronglyDedicatedIvitation]
        )

        invitation_accept = cls.as_view({
            'post': 'accept',
        },
            permission_classes=[IsHackFMIUser,
                                CanNotAcceptInvitationIfTeamLeader,
                                IsInvitedUserInTeam,
                                CanNotAccessWronglyDedicatedIvitation]
        )

        return locals()


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


class OnBoardCompetitorAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        if not request.user.get_competitor():
            serializer = OnBoardingCompetitorSerializer(data=request.data, baseuser=request.user)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"custom_errors": ["User is already competitor!"]}, status=status.HTTP_400_BAD_REQUEST)


class TestApi(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        return Response("Great, status 200", status=status.HTTP_200_OK)
