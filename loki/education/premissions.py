from rest_framework import permissions
from .models import CourseAssignment


class IsStudent(permissions.BasePermission):
    message = 'You are not a student!'

    def has_permission(self, request, view):
        try:
            is_student = request.user.get_student()
            return request.user and request.user.is_authenticated() and is_student
        except:
            return False


class IsTeacher(permissions.BasePermission):
    message = 'You are not a teacher!'

    def has_permission(self, request, view):
        try:
            is_teacher = request.user.get_teacher()
            return request.user and request.user.is_authenticated and is_teacher
        except:
            return False


class IsTeacherForCA(permissions.BasePermission):
    message = 'You dont teach that course!'

    def has_permission(self, request, view):
        ca_id = request.data['assignment']
        assignment = CourseAssignment.objects.get(id=ca_id)
        teacher = request.user.get_teacher()

        return assignment.course in teacher.teached_courses.all()
