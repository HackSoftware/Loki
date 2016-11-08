from django.db import models
from .query import SolutionQuerySet


class SolutionManager(models.Manager):
    def get_queryset(self):
        return SolutionQuerySet(self.model, using=self._db)

    def get_latest_solution(self, user, task):
        return self.get_queryset().filter(student=user, task=task).last()
