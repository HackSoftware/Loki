from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Skill, Competitor, Team, TeamMembership
from .serializers import SkillSerializer, CompetitorSerializer, TeamSerializer, Invitation, InvitationSerializer
from django.core.exceptions import ValidationError

from djoser import views
from django.conf import settings


class SkillListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        languages = Skill.objects.all()
        serializer = SkillSerializer(languages, many=True)
        return Response(serializer.data)


class CompetitorListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        competitors = Competitor.objects.all()
        serializer = CompetitorSerializer(competitors, many=True)
        return Response(serializer.data)


@permission_classes((IsAuthenticated,))
class TeamListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if 'id' in request.GET.keys():
            id = request.GET['id']
            team = Team.objects.get(id=id)
            serializer = TeamSerializer(team, many=False)
            return Response(serializer.data)
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class RegistrationView(views.RegistrationView):
    def get_serializer_class(self):
        return CompetitorSerializer

    def get_send_email_extras(self):

        return {
            'subject_template_name': settings.BASE_DIR +  '/hack_fmi/templates/activation_email_subject.txt',
            'plain_body_template_name': settings.BASE_DIR + '/hack_fmi/templates/activation_email_body.txt',
        }


class Login(views.LoginView):
    def action(self, serializer):
        user = serializer.object
        if not user.get_competitor():
            return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)
        return super(Login, self).action(serializer)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def register_team(request):
    logged_user = request.user
    serializer = TeamSerializer(data=request.data)
    if not logged_user.get_competitor():
        return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)

    if serializer.is_valid():
        if TeamMembership.objects.filter(competitor=logged_user.competitor, team__season=1).exists():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # TODO: Find a proper way to do this!
        team = serializer.save()
        team.technologies = request.data['technologies']
        team.save()

        team_membership = TeamMembership.objects.create(
            competitor=logged_user.competitor,
            team=team,
            is_leader=True
        )
        team_membership.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def me(request):
    logged_competitor = request.user.get_competitor()
    serializer = CompetitorSerializer(logged_competitor, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def leave_team(request):
    logged_competitor = request.user.get_competitor()
    TeamMembership.objects.get(competitor=logged_competitor).delete()
    return Response(status=status.HTTP_200_OK)


class InvitationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        membership = TeamMembership.objects.filter(competitor=logged_competitor).first()
        invited_competitor = Competitor.objects.filter(email=request.data['email']).first()
        if not invited_competitor:
            error = {"Error": "Този потребител все още не е регистриран в системата."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        if Invitation.objects.filter(team=membership.team, competitor=invited_competitor).first():
            error = {"Error": "Вече си изпратил покана на този участник. Изчакай отговор от него."}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if membership.is_leader:
            Invitation.objects.create(team=membership.team, competitor=invited_competitor)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitations = Invitation.objects.filter(competitor=logged_competitor)
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitation = Invitation.objects.get(id=request.data['id'])
        if invitation.competitor != logged_competitor:
            error = {"Error": "Тази покана не е за теб."}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if logged_competitor.team_set.all():
            error = {"Error": "Вече имаш отбор. Напусни го и тогава можеш да приемеш нова покана."}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        TeamMembership.objects.create(competitor=logged_competitor, team=invitation.team)
        invitation.delete()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        logged_competitor = request.user.get_competitor()
        invitation = Invitation.objects.get(id=request.data['id'])
        if invitation.competitor != logged_competitor:
            error = {"Error": "Тази покана не е за теб."}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        invitation.delete()
        return Response(status=status.HTTP_200_OK)
