from django.db import models
from django.utils import timezone

from loki.base_app.models import BaseUser


class SolutionQuerySet(models.QuerySet):

    def get_latest_solution(self, user, task):
        return self.filter(student=user, task=task).last()


class CheckInQuerySet(models.QuerySet):

    def get_student_dates(self, student, course):
        user = BaseUser.objects.get(id=student.baseuser_ptr_id)
        return self.filter(user=user,
                           date__gte=course.start_time,
                           date__lte=course.end_time).values_list(
                                              'date', flat=True)

    def get_teacher_dates(self, teacher, course):
        mac = teacher.mac
        return self.filter(mac=mac,
                           date__gte=course.start_time,
                           date__lte=course.end_time).values_list(
                                              'date', flat=True)


class CourseQuerySet(models.QuerySet):

    def get_active_courses(self):
        return self.filter(end_time__gte=timezone.now().date())

    def get_closed_courses(self):
        return self.filter(end_time__lte=timezone.now().date())
