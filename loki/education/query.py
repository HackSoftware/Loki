from django.db import models
from django.utils import timezone

from loki.base_app.models import BaseUser


class SolutionQuerySet(models.QuerySet):

    def get_solutions_for(self, user, task):
        return self.filter(student=user, task=task)


class CheckInQuerySet(models.QuerySet):

    def get_user_dates(self, user, course):
        user = BaseUser.objects.get(id=user.baseuser_ptr_id)
        return self.filter(user=user,
                           date__gte=course.start_time,
                           date__lte=course.end_time).values_list(
                                              'date', flat=True)


class CourseQuerySet(models.QuerySet):

    def get_active_courses(self):
        return self.filter(start_time__lte=timezone.now().date(),
                           end_time__gte=timezone.now().date())

    def get_closed_courses(self):
        return self.filter(end_time__lte=timezone.now().date())


class TaskQuerySet(models.QuerySet):

    def get_tasks_for(self, course, gradable=False):
        return self.filter(course=course,
                           gradable=gradable)
