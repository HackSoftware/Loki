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

        return Course.objects.filter(end_time__gte=now)


class CourseDashboardView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin, ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin, \
                   CannotSeeOthersSolutionsMixin, DetailView):
    model = Solution
    pk_url_kwarg = 'solution'
