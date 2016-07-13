from rest_framework import permissions
from datetime import date
from hack_fmi.models import (Team, Competitor, TeamMembership,
                             Season)


class IsHackFMIUser(permissions.BasePermission):
    message = "You are not a member of the HackFMI system!"

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

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

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.team.get_leader() == request.user.get_competitor()


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

    def has_object_permission(self, request, view, obj):
        return obj.season.make_team_dead_line < date.today()


class IsMentorDatePickUpToDate(permissions.BasePermission):
    message = "You cannot choose a mentor in this season's period!"

    def has_permission(self, request, view):
        if not request.data:
            return True

        today = date.today()
        team = Team.objects.get(id=request.data['team'])
        return team.season.mentor_pick_start_date < today and team.season.mentor_pick_end_date > today


class CanAttachMentors(permissions.BasePermission):
    """
    TODO: Not used
    """
    message = "This team cannot attach other members!"

    def has_object_permission(self, request, view, obj):
        return obj.mentors.all() >= obj.season.max_mentor_pick


class IsTeamInActiveSeason(permissions.BasePermission):
    message = "This team is not in an active season!"

    def has_object_permission(self, request, view, obj):
        return obj.season.is_active is True


class IsTeamleaderOrCantCreate(permissions.BasePermission):
    message = "Only team leaders can invite members to team"

    def has_permission(self, request, view):

        if request.method == "POST":
            user = request.user.get_competitor()
            return TeamMembership.objects.filter(competitor=user, is_leader=True).exists()

        """
        TODO: **Short** explanation why we are returning True
        """
        return True


class IsInvitedMemberAlreadyInYourTeam(permissions.BasePermission):

    message = "The member you are trying to add is already in your team!!"

    def has_permission(self, request, view):
        if request.method == "POST":
            competitor = Competitor.objects.filter(email=request.data['competitor_email'])
            leader_team = TeamMembership.objects.get(competitor=request.user).team
            return TeamMembership.objects.filter(competitor=competitor, team=leader_team).count() == 0

        """
        TODO: **Short** explanation why we are returning True
        """
        return True


class IsInvitedMemberAlreadyInOtherTeam(permissions.BasePermission):

    message = '''You you have already been a member of any existing team.
                 Please leave that team and then in order to accept the invitation!'''

    def has_permission(self, request, view):
        if request.method == "POST":
            competitor = Competitor.objects.filter(email=request.data['competitor_email'])
            return TeamMembership.objects.filter(competitor=competitor).count() == 0

        """
        TODO: **Short** explanation why we are returning True
        """
        return True


class CanInviteMoreMembers(permissions.BasePermission):
    active_season = Season.objects.get(is_active=True)

    message = "You cannot invite more than {} in your team".format(active_season.max_team_members_count)

    def has_permission(self, request, view):
        if request.method == "POST":
            user_team = TeamMembership.objects.get(competitor=request.user).team
            members_in_team = TeamMembership.objects.filter(team=user_team).count()

            return members_in_team < user_team.season.max_team_members_count

        """
        TODO: **Short** explanation why we are returning True
        """
        return True


class IsInvitationNotForLoggedUser(permissions.BasePermission):

    message = "This invitation is not dedicated to you!"

    def has_object_permission(self, request, view, obj):
        if TeamMembership.objects.filter(competitor=request.user, is_leader=True).count() != 0:
            return True

        return request.user.get_competitor() == obj.competitor


class IsInvitedUserInTeam(permissions.BasePermission):

    message = "You have already been a member in another team!"

    def has_object_permission(self, request, view, obj):
        return not TeamMembership.objects.filter(competitor=obj.competitor).exists()


class CanNotAcceptIfTeamLeader(permissions.BasePermission):

    message = "You are a leader of your team and cannot accept any invitations!"

    def has_object_permission(self, request, view, obj):
        return not TeamMembership.objects.filter(competitor=request.user, is_leader=True).exists()
