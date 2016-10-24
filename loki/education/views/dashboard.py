from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from loki.education.models import Course, Task, Solution, Student
from ..mixins import DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin
from rest_framework import serializers


class CourseListView(DashboardPermissionMixin, ListView):
    model = Course

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
            context['tasksolution'].update({task_name: solution})
        return context

    def get_queryset(self):
        return Task.objects.filter(course=self.course).order_by('week')

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code', None)
        task_id = request.POST.get('task_id', None)
        course_id = kwargs.get('course')

        '''
            Solutions without code are not accepted
        '''
        if not code:
            raise serializers.ValidationError('Either code, file or url should be given.')

        task = Task.objects.get(id=task_id)
        student = Student.objects.get(email=request.user.email)
        Solution.objects.create(task=task, student=student, status=Solution.PENDING)

        return redirect(reverse('education:course_dashboard', kwargs={'course': course_id}))


class SolutionView(DashboardPermissionMixin, CannotSeeOthersCoursesDashboardsMixin,
                   ListView):
    model = Solution

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs.get("task"))
        return Solution.objects.filter(student=self.request.user, task=task).order_by("-created_at")
