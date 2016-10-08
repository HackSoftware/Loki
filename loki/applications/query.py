from django.db import models


class ApplicationQuerySet(models.QuerySet):

    def without_interviews(self):
        return self.filter(has_interview_date=False)

    def without_interviews_for(self, application_info):
        return self.without_interviews().filter(
               application_info=application_info)

class ApplicationInfoQuerySet(models.QuerySet):

    def with_interview_dates(self):
        return self.filter(start_interview_date__isnull=False).filter(
                           end_interview_date__isnull=False)
