from django.db import models


class SolutionQuerySet(models.QuerySet):

    def get_latest_solution(self, user, task):
        return self.filter(student=user, task=task).last()

class CheckInQuerySet(models.QuerySet):

    def get_student_dates(self, student, course):
        return self.filter(student=student,
                           date__gte=course.start_time,
                           date__lte=course.end_time).values_list(
                                              'date', flat=True)
