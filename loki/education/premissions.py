from rest_framework import permissions
from .models import CourseAssignment, Course
from django.shortcuts import get_object_or_404


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


class IsTeacherForThisCourse(permissions.BasePermission):
    message = 'You are not the teacher of this course'

    def has_permission(self, request, view):
        teacher = request.user.get_teacher()
        course = get_object_or_404(Course, id=request.data['course__id'])
        return course in teacher.teached_courses.all()
