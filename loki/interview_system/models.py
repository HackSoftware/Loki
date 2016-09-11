from django.db import models

from loki.base_app.models import BaseUser
from loki.applications.models import ApplicationInfo, Application


class Interviewer(BaseUser):

    courses_to_interview = models.ManyToManyField(ApplicationInfo)
    interviews = models.ManyToManyField(Application, through='Interview')


class InterviewerFreeTime(models.Model):

    interviewer = models.ForeignKey(Interviewer)
    date = models.DateField(blank=False, null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)

    def __str__(self):
        return "On " + str(self.date) + " - from " + str(self.start_time) + " to " + str(self.end_time)


class Interview(models.Model):

    interviewer = models.ForeignKey(Interviewer)
    application = models.ForeignKey(Application)
    date = models.DateField(blank=False, null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)
    has_confirmed = models.BooleanField(default=False)
    has_received_email = models.BooleanField(default=False)
