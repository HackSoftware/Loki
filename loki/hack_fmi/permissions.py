from rest_framework import permissions
from datetime import date
from hack_fmi.models import Team


class IsHackFMIUser(permissions.BasePermission):
    message = "You are not a member of the HackFMI system!"

    def has_permission(self, request, view):
        try:
            is_hackfmi_user = request.user.get_competitor()
            return request.user and request.user.is_authenticated() and is_hackfmi_user
        except:
            return False


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
    message = "This team cannot attach other members!"

    def has_object_permission(self, request, view, obj):
        return obj.mentors.all() >= obj.season.max_mentor_pick


class IsTeamInActiveSeason(permissions.BasePermission):
    message = "This team is not in an active season!"

    def has_object_permission(self, request, view, obj):

        return obj.season.is_active is True
