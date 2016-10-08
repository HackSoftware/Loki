from django.db import models
from .query import ApplicationInfoQuerySet


class ApplicationInfoManager(models.Manager):
    """
    TODO: Write tests
    """
    def get_queryset(self):
        return ApplicationInfoQuerySet(self.model, using=self._db)

    def get_open_for_apply(self):
        return [info for info in self.all() if info.apply_is_active()]

    def get_closed_for_apply(self):
        return [info for info in self.all() if not info.apply_is_active()]

    def get_open_for_interview(self):
        return [info for info in self.get_queryset().with_interview_dates()
                if info.interview_is_active()]
