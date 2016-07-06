from rest_framework import permissions
from datetime import date


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
