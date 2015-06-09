from rest_framework import permissions


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            is_student = request.user.get_student()
            return request.user and request.user.is_authenticated() and is_student
        except:
            return False
