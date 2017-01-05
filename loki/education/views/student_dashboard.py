from django.views.generic.list import ListView
from loki.education.models import Course, Task, Solution
from loki.education.mixins import (DashboardPermissionMixin,
                      CannotSeeOthersCoursesDashboardsMixin,
                      CannotSeeCourseTaskListMixin)
from loki.education.helper import task_solutions, latest_solution_statuses


class TaskListView(DashboardPermissionMixin,
                   CannotSeeOthersCoursesDashboardsMixin,
                   CannotSeeCourseTaskListMixin,
                   ListView):
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
        return Task.objects.filter(course=self.course).order_by('-week')

    def post(self, request, *args, **kwargs):
        url = self.request.POST['url']
        task_id = self.request.POST['task']
        task = Task.objects.filter(id=task_id).first()
        Solution.objects.create(student=self.request.user.student,
                                url=url,
                                task=task)

        return super().get(request, *args, **kwargs)


class SolutionListView(DashboardPermissionMixin,
                       CannotSeeOthersCoursesDashboardsMixin,
                       ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.kwargs.get('course')
        context['course'] = Course.objects.get(id=course)
        return context
