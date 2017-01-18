from django.views.generic.list import ListView
from django.views.generic import TemplateView
from loki.education.models import Course, Material, CheckIn
from loki.education.mixins import (DashboardPermissionMixin,
                                   CannotSeeOthersCoursesDashboardsMixin)
from loki.education.helper import get_dates_for_weeks, percentage_presence
from loki.education.services import get_course_presence

class CourseListView(DashboardPermissionMixin,
                     TemplateView):

    template_name = 'education/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_courses'] = None
        context['student_courses'] = None
        if self.request.user.get_teacher():
            context['teacher_courses'] = self.request.user.teacher.teached_courses.all()

        if self.request.user.get_student():
            context['student_courses'] = Course.objects.filter(
                courseassignment__user=self.request.user).order_by('-end_time')

        user = self.request.user.get_student() if self.request.user.get_student() else self.request.user.get_teacher()

        course_presence = {}
        if context['teacher_courses']:
            for course in context['teacher_courses']:
                if course.lecture_set.exists():
                    course_presence[course] = get_course_presence(course=course, user=user)

        if context['student_courses']:
            for course in context['student_courses']:
                if course.lecture_set.exists():
                    course_presence[course] = get_course_presence(course=course, user=user)

        context['course_presence'] = course_presence

        return context


class MaterialListView(DashboardPermissionMixin,
                       CannotSeeOthersCoursesDashboardsMixin,
                       ListView):
    model = Material

    def get_queryset(self):
        return Material.objects.filter(course=self.course).order_by("-week")
