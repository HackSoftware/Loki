from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from loki.education.models import Course, Task, Solution, Student, CheckIn, Lecture
from ..mixins import DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin
from rest_framework import serializers
from ..serializers import CheckInSerializer
from ..helper import get_weeks_for_course, get_dates_for_weeks, get_student_dates

class CourseListView(DashboardPermissionMixin, ListView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student

        for course in self.get_queryset():
            context['weeks'] = list(set(get_weeks_for_course(course)))
            context['dates_for_weeks'] = get_dates_for_weeks(course)
            context['student_dates'] = get_student_dates(student, course)

        return context

    def get_queryset(self):
        now = timezone.now().date()

        return Course.objects.filter(end_time__gte=now,
                                     courseassignment__user=self.request.user)


class CourseDashboardView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solutions = Solution.objects.filter(student=self.request.user)
        context['tasksolution'] = {}
        for solution in solutions:
            task_name = solution.task.name
            if task_name in context['tasksolution']:
                context['tasksolution'][task_name].append(solution)
            else:
                context['tasksolution'].update({task_name: solution})
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")
