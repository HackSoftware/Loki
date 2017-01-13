from django.views.generic.list import ListView

from loki.education.models import Course, Material
from loki.education.mixins import (DashboardPermissionMixin,
                                   CannotSeeOthersCoursesDashboardsMixin)
from loki.education.services import get_course_presence


class CourseListView(DashboardPermissionMixin,
                     ListView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.get_student():
            user = self.request.user.student
        else:
            user = self.request.user.teacher

        course_presence = {}
        for course in self.get_queryset():
            if not course.lecture_set.exists():
                continue
            course_presence[course] = {}
            course_presence[course] = get_course_presence(course, user)
        context['course_presence'] = course_presence

        return context

    def get_queryset(self):
        if self.request.user.get_teacher():
            return self.request.user.teacher.teached_courses.all()
        if self.request.user.get_student():
            return Course.objects.filter(courseassignment__user=self.request.user).order_by('-end_time')


class MaterialListView(DashboardPermissionMixin,
                       CannotSeeOthersCoursesDashboardsMixin,
                       ListView):
    model = Material

    def get_queryset(self):
        return Material.objects.filter(course=self.course).order_by("-week")
