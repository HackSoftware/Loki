from django.db import models
from django.utils import timezone


class SolutionQuerySet(models.QuerySet):

    def get_latest_solution(self, user, task):
        return self.filter(student=user, task=task).last()


class CheckInQuerySet(models.QuerySet):

    def get_student_dates(self, student, course):
        return self.filter(student=student,
                           date__gte=course.start_time,
                           date__lte=course.end_time).values_list(
                                              'date', flat=True)


class CourseQuerySet(models.QuerySet):

    def get_active_courses(self):
        return self.filter(start_time__lte=timezone.now().date(),
                           end_time__gte=timezone.now().date())

    def get_closed_courses(self):
        return self.filter(end_time__lte=timezone.now().date())
