from django.db import models


class InterviewQuerySet(models.QuerySet):

    def get_free_slots(self):
        return self.filter(application__isnull=True)
