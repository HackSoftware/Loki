from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ParseError
from rest_framework import mixins
from rest_framework_jwt.views import RefreshJSONWebToken
from django.core.exceptions import ObjectDoesNotExist

from .models import (Skill, Team, TeamMembership, TeamMentorship,
                     Mentor, Season, Competitor,
                     BlackListToken, SeasonCompetitorInfo)
from .serializers import (SkillSerializer, TeamSerializer, Invitation,
                          InvitationSerializer, MentorSerializer,
                          SeasonSerializer, PublicTeamSerializer,
                          OnBoardingCompetitorSerializer,
                          SeasonCompetitorInfoSerializer,
                          TeamMembershipSerializer,
                          TeamMentorshipSerializer,
                          CompetitorListSerializer,
                          CustomTeamSerializer)

from .permissions import (CanAttachMoreMentorsToTeam,
                          CanInviteMoreMembersInTeam,
                          IsHackFMIUser, IsMemberOfTeam,
                          TeamLeaderCantCreateOtherTeam,
                          CantChangeOtherCompetitorsData,
                          IsTeamMembershipInActiveSeason,
                          IsInvitedMemberAlreadyInYourTeam,
                          IsInvitedMemberAlreadyInOtherTeam,
                          CanNotAcceptInvitationIfTeamLeader,
                          IsInvitedUserInTeam, IsSeasonActive,
                          CanNotAccessWronglyDedicatedIvitation,
                          IsTeamLeader, IsSeasonDeadlineUpToDate,
                          IsCompetitorMemberOfTeamForActiveSeason,
                          CantCreateTeamWithTeamNameThatAlreadyExists,
                          IsInvitedMemberCompetitor, IsTeamLeaderOrReadOnly,
                          IsMentorDatePickUpToDate, IsTeamleaderOrCantCreateIvitation,
                          MentorIsAlreadySelectedByThisTeamLeader,
                          )

from .helper import send_team_delete_email, send_invitation, get_object_variable_or_none
from .mixins import MeSerializerMixin, JwtApiAuthenticationMixin

from loki.base_app.helper import try_open

import json


class MeAPIView(JwtApiAuthenticationMixin,
                MeSerializerMixin,
                generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)
        teams_data = None
        data["teams"] = teams_data

        if not data['is_competitor']:
            return Response(data=data, status=status.HTTP_200_OK)

        competitor = self.request.user.get_competitor()
        teams = TeamMembership.objects.list_all_teams_for_competitor(competitor=competitor)

        if teams:
            teams_data = CustomTeamSerializer(teams, many=True).data

        data["teams"] = teams_data

        return Response(data=data, status=status.HTTP_200_OK)


class MeSeasonAPIView(JwtApiAuthenticationMixin,
                      MeSerializerMixin,
                      generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs)

        team_data = None
        data["team"] = None

        if not data['is_competitor']:
            return Response(data=data, status=status.HTTP_200_OK)

        season_id = self.kwargs.get('season_pk')
        season = get_object_or_404(Season, pk=season_id)

        competitor = self.request.user.get_competitor()
        team = Team.objects.get_all_teams_for_current_season(season=season).\
            get_all_teams_for_competitor(competitor=competitor).first()

        tm_id = None

        if team:
            team_data = CustomTeamSerializer(team).data
            tm_id = get_object_variable_or_none(
                queryset=TeamMembership.objects.filter(team=team, competitor=competitor),
                variable="id")

        data["team"] = team_data
        data["team_membership_id"] = tm_id

        try:
            season_competitor_info = SeasonCompetitorInfo.objects.get(competitor=competitor)
            looking_for_team = season_competitor_info.looking_for_team
            season_competitor_info_id = season_competitor_info.id
        except ObjectDoesNotExist:
            looking_for_team = False
            season_competitor_info_id = None

        data["looking_for_team"] = looking_for_team
        data["season_competitor_info_id"] = season_competitor_info_id

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


class TeamAPI(JwtApiAuthenticationMixin,
              mixins.CreateModelMixin,
              mixins.ListModelMixin,
              mixins.UpdateModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.filter(season__is_active=True)

    """
    Get away from overriding JwtApiAuthenticationMixin'permission classes
    """

    def get_permissions(self):
        permission_classes = (IsHackFMIUser, IsTeamLeaderOrReadOnly,
                              IsSeasonDeadlineUpToDate,
                              CantCreateTeamWithTeamNameThatAlreadyExists,
                              TeamLeaderCantCreateOtherTeam)
        self.permission_classes += super().permission_classes + permission_classes

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        season = Season.objects.get(is_active=True)
        team = serializer.save(season=season)
        team.add_member(self.request.user.get_competitor(), is_leader=True)
        team.save()


class TeamMembershipAPI(JwtApiAuthenticationMixin,
                        generics.DestroyAPIView):
    serializer_class = TeamMembershipSerializer

    def get_permissions(self):
        self.permission_classes += super().permission_classes + (IsHackFMIUser, IsMemberOfTeam,
                                                                 IsTeamMembershipInActiveSeason,)

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return TeamMembership.objects.all()

    def perform_destroy(self, instance):
        # Remove team if teamleader leaves
        if instance.is_leader is True:
            team = instance.team
            send_team_delete_email(team)
            team.delete()
        instance.delete()


class TeamMentorshipAPI(JwtApiAuthenticationMixin,
                        mixins.DestroyModelMixin,
                        generics.CreateAPIView):

    serializer_class = TeamMentorshipSerializer
    queryset = TeamMentorship.objects.all()

    def get_permissions(self):
        permission_classes = (IsHackFMIUser, IsTeamLeader,
                              IsMentorDatePickUpToDate,
                              CanAttachMoreMentorsToTeam,
                              MentorIsAlreadySelectedByThisTeamLeader)

        self.permission_classes += super().permission_classes + permission_classes

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        team = TeamMembership.objects.get_team_memberships_for_active_season(
            competitor=self.request.user.get_competitor()).first().team

        serializer.save(team=team)

    def get_object(self):
        competitor = self.request.user.get_competitor()
        team = TeamMembership.objects.get_team_memberships_for_active_season(
            competitor=competitor).first().team
        mentor = get_object_or_404(Mentor, id=self.kwargs['mentor_pk'])
        teammentor_ship = TeamMentorship.objects.filter(team=team, mentor=mentor)

        if not teammentor_ship.exists():
            raise ParseError(detail="You can't delete non-selected mentor.")

        return teammentor_ship.first()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InvitationViewSet(JwtApiAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = InvitationSerializer

    list_permission_classes = (IsHackFMIUser,
                               IsTeamleaderOrCantCreateIvitation,
                               IsInvitedMemberCompetitor,
                               IsInvitedMemberAlreadyInYourTeam,
                               IsInvitedMemberAlreadyInOtherTeam,
                               CanInviteMoreMembersInTeam)

    detail_permission_classes = (IsHackFMIUser,
                                 CanNotAccessWronglyDedicatedIvitation)

    accept_permission_classes = (IsHackFMIUser,
                                 CanNotAcceptInvitationIfTeamLeader,
                                 IsInvitedUserInTeam,
                                 CanNotAccessWronglyDedicatedIvitation)

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
        return Response("You have accepted this invitation!", status=status.HTTP_200_OK)

    @classmethod
    def get_urls(cls):
        invitation_list = cls.as_view({
            'get': 'list',
            'post': 'create',
        },
            permission_classes=cls.permission_classes + cls.list_permission_classes
        )

        invitation_detail = cls.as_view({
            'delete': 'destroy',
        },
            permission_classes=cls.permission_classes + cls.detail_permission_classes
        )

        invitation_accept = cls.as_view({
            'post': 'accept',
        },
            permission_classes=cls.permission_classes + cls.accept_permission_classes
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


class OnBoardCompetitorAPI(JwtApiAuthenticationMixin,
                           APIView):

    def post(self, request, format=None):
        if not request.user.get_competitor():
            serializer = OnBoardingCompetitorSerializer(data=request.data, baseuser=request.user)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"custom_errors": ["User is already competitor!"]}, status=status.HTTP_400_BAD_REQUEST)


class TestApi(JwtApiAuthenticationMixin,
              APIView):

    def get(self, request):
        return Response("Great, status 200", status=status.HTTP_200_OK)


class SeasonInfoAPI(JwtApiAuthenticationMixin,
                    generics.CreateAPIView,
                    generics.UpdateAPIView):
    serializer_class = SeasonCompetitorInfoSerializer
    queryset = SeasonCompetitorInfo.objects.filter(season__is_active=True)

    def get_permissions(self):
        permission_classes = (IsSeasonActive, IsCompetitorMemberOfTeamForActiveSeason,
                              CantChangeOtherCompetitorsData)
        self.permission_classes += super().permission_classes + permission_classes
        return [permission() for permission in self.permission_classes]


class CompetitorListAPIView(JwtApiAuthenticationMixin, generics.ListAPIView):
    serializer_class = CompetitorListSerializer

    def get_permissions(self):
        permission_classes = (IsTeamLeader, IsTeamMembershipInActiveSeason,
                              CanInviteMoreMembersInTeam)
        self.permission_classes += super().permission_classes + permission_classes
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return Competitor.objects.filter(seasoncompetitorinfo__season__is_active=True,
                                         seasoncompetitorinfo__looking_for_team=True)


class JWTLogoutView(JwtApiAuthenticationMixin,
                    APIView):

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')

        if BlackListToken.objects.filter(token=token).exists():
            return Response("Token is already blacklisted.", status=status.HTTP_400_BAD_REQUEST)

        BlackListToken.objects.create(token=token)
        return Response("Token has been blacklisted.", status=status.HTTP_202_ACCEPTED)


class CustomRefreshJSONWebTokenAPIView(JwtApiAuthenticationMixin, RefreshJSONWebToken):

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        BlackListToken.objects.create(token=token)

        return super().post(request, *args, **kwargs)
