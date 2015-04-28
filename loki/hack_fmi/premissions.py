from rest_framework import permissions


class IsHackFMIUser(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            is_hackfmi_user = request.user.get_competitor()
            return request.user and request.user.is_authenticated() and is_hackfmi_user
        except:
            return False


class IsTeamLeaderOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.get_leader() == request.user.get_competitor()
