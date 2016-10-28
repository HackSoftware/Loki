from django.views.generic.list import ListView
from django.utils import timezone

from loki.education.models import Course, Task, Solution
from ..mixins import (DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                      CannotSeeCourseTaskListMixin)
from ..helper import (get_weeks_for_course, get_dates_for_weeks, get_student_dates,
                      task_solutions)


class CourseListView(DashboardPermissionMixin, ListView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        course_presence = {}

        for course in self.get_queryset():
            course_presence[course] = {}
            course_presence[course]['weeks'] = list(set(get_weeks_for_course(course)))
            course_presence[course]['dates_for_weeks'] = get_dates_for_weeks(course)
            course_presence[course]['student_dates'] = get_student_dates(student, course)

        context['course_presence'] = course_presence
        return context

    def get_queryset(self):
        now = timezone.now().date()

        return Course.objects.filter(end_time__gte=now,
                                     courseassignment__user=self.request.user)


class CourseDashboardView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                          CannotSeeCourseTaskListMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.kwargs.get('course')
        solutions = Solution.objects.filter(student=self.request.user.student).filter(
                                            task__course__in = [course])
        context['tasksolution'] = task_solutions(solutions)
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")
