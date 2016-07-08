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
                          IsInvitationSentToInvitedMember,
                          IsInvitedMemberAlreadyInYourTeam)
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
                          CanInviteMoreMembers)

    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(competitor=self.request.user,
                                         team__season__is_active=True)

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









    # def post(self, request, format=None):
        # logged_competitor = request.user.get_competitor()
        # current_season = Season.objects.get(is_active=True)
        # membership = TeamMembership.objects.get(competitor=logged_competitor, team__season=current_season)
        # invited_competitor = Competitor.objects.filter(email=request.data['email']).first()
        # if not invited_competitor:
        #     error = {"error": "Този потребител все още не е регистриран в системата."}
        #     return Response(error, status=status.HTTP_403_FORBIDDEN)
        # if Invitation.objects.filter(team=membership.team, competitor=invited_competitor).first():
        #     error = {"error": "Вече си изпратил покана на този участник. Изчакай да потвърди!"}
        #     return Response(error, status=status.HTTP_403_FORBIDDEN)

        # if membership.team in invited_competitor.team_set.all():
        #     error = {"error": "Този участник вече е в отбора ти!"}
        #     return Response(error, status=status.HTTP_403_FORBIDDEN)

        # if len(membership.team.teammembership_set.all()) >= current_season.max_team_members_count:
        #     error = {"error": "В този отбор вече има повече от 6 човека. "
        #                       "Трябва някой да напусне отбора за да можеш да приемш тази покана!"}
        #     return Response(error, status=status.HTTP_403_FORBIDDEN)

        # if membership.is_leader:
        #     Invitation.objects.create(team=membership.team, competitor=invited_competitor)
        #     message = {"message": "Успешно изпратихте поканата за включване в отбора!"}
        #     sender = settings.DEFAULT_FROM_EMAIL
        #     mail.send(
        #         invited_competitor.email,
        #         sender,
        #         template='hackfmi_team_invite',
        #     )
        #     return Response(message, status=status.HTTP_201_CREATED)
        # message = {"message": "Трябва да бъдете лидер, за да каните хора!"}
        # return Response(message, status=status.HTTP_403_FORBIDDEN)

    # def put(self, request, format=None):
    #     logged_competitor = request.user.get_competitor()
    #     invitation = Invitation.objects.get(id=request.data['id'])
    #     current_season = Season.objects.get(is_active=True)
    #     if invitation.competitor != logged_competitor:
    #         error = {"error": "Тази покана не е за теб."}
    #         return Response(error, status=status.HTTP_403_FORBIDDEN)
    #     if logged_competitor.team_set.filter(season=current_season):
    #         error = {"error": "Вече имаш отбор. Напусни го и тогава можеш да приемеш нова покана."}
    #         return Response(error, status=status.HTTP_403_FORBIDDEN)

    #     TeamMembership.objects.create(competitor=logged_competitor, team=invitation.team)
    #     invitation.delete()
    #     message = {"message": "Успешно се присъединихте към отбора."}
    #     return Response(message, status=status.HTTP_200_OK)

    # def delete(self, request, format=None):
    #     logged_competitor = request.user.get_competitor()
    #     invitation = Invitation.objects.get(id=request.data['id'])
    #     if invitation.competitor != logged_competitor:
    #         error = {"error": "Тази покана не е за теб."}
    #         return Response(error, status=status.HTTP_403_FORBIDDEN)
    #     invitation.delete()
    #     return Response(status=status.HTTP_200_OK)


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
