from rest_framework import permissions
from datetime import date

from .models import (Team, Competitor, TeamMembership,
                     Season, TeamMentorship)


class IsHackFMIUser(permissions.BasePermission):
    message = "You are not a member of the HackFMI system!"

    def has_permission(self, request, view):
        is_hackfmi_user = request.user.get_competitor()
        return request.user and is_hackfmi_user


class IsTeamLeaderOrReadOnly(permissions.BasePermission):
    message = "You are not a leader of this team!"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.get_leader() == request.user.get_competitor()


class IsTeamLeader(permissions.BasePermission):
    message = "You are not a leader of this team!"

    def has_permission(self, request, view):
        if request.method == 'POST':
            team = Team.objects.get_team_by_id(id=request.data['team']).first()
            competitor = request.user.get_competitor()
            return TeamMembership.objects.is_competitor_leader_of_team(competitor=competitor, team=team)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method != 'POST':
            return obj.team.get_leader() == request.user.get_competitor()

        return True


class IsMemberOfTeam(permissions.BasePermission):
    message = "You are not a member of this team!"

    def has_object_permission(self, request, view, obj):
        return obj.competitor == request.user.get_competitor()


class IsTeamMembershipInActiveSeason(permissions.BasePermission):
    message = "This team is not in an active season!"

    def has_object_permission(self, request, view, obj):
        return obj.team.season.is_active is True


class IsSeasonDeadlineUpToDate(permissions.BasePermission):
    message = "The deadline for creating new teams has expired!"

    def has_permission(self, request, view):
        if request.method == "POST":
            active_season = Season.objects.get(is_active=True)
            return active_season.make_team_dead_line > date.today()
        return True


class IsMentorDatePickUpToDate(permissions.BasePermission):
    message = "You cannot choose a mentor in this season's period!"

    def has_permission(self, request, view):
        if not request.data:
            return True

        today = date.today()
        team = Team.objects.get(id=request.data['team'])
        return team.season.mentor_pick_start_date < today and team.season.mentor_pick_end_date > today


class CanAttachMoreMentorsToTeam(permissions.BasePermission):
    message = "This team cannot attach other mentors!"

    def has_permission(self, request, view):
        if request.method == 'POST':
            team = Team.objects.get_team_by_id(id=request.data['team']).first()
            max_mentors_pick = team.season.max_mentor_pick
            mentors_for_current_team = TeamMentorship.objects.get_all_team_mentorships_for_team(team=team).count()
            return max_mentors_pick > mentors_for_current_team
        # If request.method = 'DELETE'
        return True


class CantCreateTeamWithTeamNameThatAlreadyExists(permissions.BasePermission):
    message = "A team with that name already exists!"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        """
        We check whether a team with that name alredy exists when we register or change a team
        (POST and PATCH), otherwise we return True.
        """
        new_name_of_team = request.data.get('name') if request.data.get('name') else None

        if request.method == "PATCH" and new_name_of_team and new_name_of_team != view.get_object().name:
            qs = Team.objects.get_team_by_name_for_active_season(name=new_name_of_team)
            return not qs.exists()

        if request.method == "POST":
            qs = Team.objects.get_team_by_name_for_active_season(name=new_name_of_team)
            return not qs.exists()

        return True


class TeamLiederCantCreateOtherTeam(permissions.BasePermission):
    message = "You are a teamleader and cant register another team!"

    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user.get_competitor()
            return not TeamMembership.objects.is_competitor_leader_in_current_season(competitor=user)
        """
        TeamLeaders cant send POST queries in order to register another team, since they have their own one.
        TeamLeaders can only change and see their own teams(GET and PATCH queries return True)
        """
        return True


class IsTeamInActiveSeason(permissions.BasePermission):
    message = "This team is not in an active season!"

    def has_object_permission(self, request, view, obj):
        return obj.season.is_active is True


class IsTeamleaderOrCantCreateIvitation(permissions.BasePermission):
    message = "Only cureent season team leaders can invite members to team"

    def has_permission(self, request, view):
        if request.method == "POST":
            user = request.user.get_competitor()
            return TeamMembership.objects.is_competitor_leader_in_current_season(competitor=user)

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class IsInvitedMemberAlreadyInYourTeam(permissions.BasePermission):

    message = "The member you are trying to add is already in your team!!"

    def has_permission(self, request, view):
        if request.method == "POST":
            leader_team = TeamMembership.objects.\
                get_all_team_memberships_for_competitor(competitor=request.user.get_competitor()).first().team
            competitor = Competitor.objects.get_competitor_by_email(email=request.data['competitor_email'])
            return not TeamMembership.objects.\
                get_all_team_memberships_for_competitor(competitor=competitor).\
                get_all_team_memberships_for_team(team=leader_team).exists()

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class IsInvitedMemberAlreadyInOtherTeam(permissions.BasePermission):

    message = '''This competitor have already been a member of any existing team.
                 Please leave that team and then in order to accept the invitation!'''

    def has_permission(self, request, view):
        if request.method == "POST":
            competitor = Competitor.objects.get_competitor_by_email(email=request.data['competitor_email'])
            return TeamMembership.objects.get_all_team_memberships_for_competitor(competitor=competitor).count() == 0

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class CanInviteMoreMembersInTeam(permissions.BasePermission):

    def __getattr__(self, name):
        """
        Since https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/views.py#L320
        is calling getattr and we want to have a good message with the max number of mentors
        We redefine __getattr__ to return the proper message when getattr(permission, 'message', None) is called.
        This is bad design from DRF.
        """
        if name == 'message':
            active_season = Season.objects.get(is_active=True)

            message = "You cannot invite more than {} in your team".format(active_season.max_team_members_count)
            return message

        return object.__getattribute__(self, name)

    def has_permission(self, request, view):
        if request.method == "POST":
            user_team = TeamMembership.objects.get(competitor=request.user.get_competitor()).team
            members_in_team = TeamMembership.objects.get_all_team_memberships_for_team(team=user_team).count()

            return members_in_team < user_team.season.max_team_members_count

        """
        Return True if you just want to see all the invitations without creating a new invitation.
        """
        return True


class CanNotAccessWronglyDedicatedIvitation(permissions.BasePermission):

    message = "This invitation is not dedicated to you!"

    def has_object_permission(self, request, view, obj):
        return request.user.get_competitor() == obj.competitor


class IsInvitedUserInTeam(permissions.BasePermission):

    message = "You have already been a member in another team!"

    def has_object_permission(self, request, view, obj):
        return not TeamMembership.objects.\
            get_team_memberships_for_active_season(competitor=request.user.get_competitor()).exists()


class CanNotAcceptInvitationIfTeamLeader(permissions.BasePermission):

    message = "You are a leader of your team and cannot accept any invitations!"

    def has_object_permission(self, request, view, obj):
        competitor = request.user.get_competitor()
        return not TeamMembership.objects.is_competitor_leader_in_current_season(competitor=competitor)


class IsInvitedMemberCompetitor(permissions.BasePermission):

    message = "Competitor with this email does not exists!!"

    def has_permission(self, request, view):
        if request.method == "POST":
            return Competitor.objects.get_competitor_by_email(email=request.data['competitor_email']).exists()
        return True
