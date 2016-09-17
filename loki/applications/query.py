from django.db import models


class ApplicationQuerySet(models.QuerySet):

    def without_interviews(self):
        return self.filter(has_interview_date=False)
