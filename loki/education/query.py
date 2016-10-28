from django.db import models


class SolutionQuerySet(models.QuerySet):

    def get_latest_solution(self, user, task):
        return self.filter(student=user, task=task).last()
