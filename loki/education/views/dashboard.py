from django.views.generic.list import ListView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponseForbidden

from loki.education.models import Course, Task, CourseAssignment, Solution
from ..mixins import (DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                      CannotSeeOthersSolutionsMixin)


class CourseListView(DashboardPermissionMixin, ListView):
    model = Course

    def get_queryset(self):
        now = timezone.now().date()

        return Course.objects.filter(end_time__gte=now, \
                                     courseassignment__user=self.request.user)


class CourseDashboardView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solutions = Solution.objects.filter(student=self.request.user)
        context['tasksolution'] = {}
        for solution in solutions:
            task_name = solution.task.name
            context['tasksolution'].update({task_name:solution})
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin, \
                   CannotSeeOthersSolutionsMixin, DetailView):
    model = Solution
    pk_url_kwarg = 'solution'
