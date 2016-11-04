from django.views.generic.list import ListView
from django.utils import timezone

from loki.education.models import Course, Task, Solution, Material, CheckIn
from ..mixins import (DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                      CannotSeeCourseTaskListMixin)
from ..helper import (get_dates_for_weeks, task_solutions,
                      latest_solution_statuses, percentage_presence)


class CourseListView(DashboardPermissionMixin, ListView):

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        course_presence = {}

        for course in self.get_queryset():
            if not course.lecture_set.exists():
                continue

            course_presence[course] = {}
            course_presence[course]['weeks'] = list(get_dates_for_weeks(course).keys())
            course_presence[course]['dates_for_weeks'] = get_dates_for_weeks(course)
            course_presence[course]['student_dates'] = CheckIn.objects.get_student_dates(student, course)
            student_dates = course_presence[course]['student_dates']
            course_presence[course]['percentage_presence'] = percentage_presence(student_dates, course)

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
                                            task__course__in=[course])
        context['tasksolution'] = task_solutions(solutions)
        tasks = Task.objects.filter(course=self.course)
        context['latest_solutions'] = latest_solution_statuses(self.request.user.student,
                                                               tasks)
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')

    def post(self, request, *args, **kwargs):
        url = self.request.POST['url']
        task_id = self.request.POST['task']
        task = Task.objects.filter(id=task_id).first()
        Solution.objects.create(student=self.request.user.student,
                                url=url,
                                task=task)

        return super().get(request, *args, **kwargs)


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")


class MaterialView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Material

    def get_queryset(self):
        return Material.objects.filter(course=self.course).order_by("week")
