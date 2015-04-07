from rest_framework import permissions


class IsHackFMIUser(permissions.BasePermission):

    def has_permission(self, request, view):
        is_hackfmi_user = request.user.get_competitor()
        return request.user and request.user.is_authenticated and is_hackfmi_user
