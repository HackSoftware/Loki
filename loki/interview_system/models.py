from django.db import models

from loki.base_app.models import BaseUser
from loki.applications.models import ApplicationInfo, Application

from .query import InterviewQuerySet


class Interviewer(BaseUser):
    courses_to_interview = models.ManyToManyField(ApplicationInfo)
    interviews = models.ManyToManyField(Application, through='Interview')


class InterviewerFreeTime(models.Model):
    interviewer = models.ForeignKey(Interviewer)
    date = models.DateField(blank=False, null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)
    buffer_time = models.BooleanField(default=False)

    def __str__(self):
        return "On " + str(self.date) + " - from " + str(self.start_time) + " to " + str(self.end_time)

    def has_generated_slots(self):
        return self.interview_set.exists()


class Interview(models.Model):
    interviewer = models.ForeignKey(Interviewer)
    application = models.ForeignKey(Application, null=True)
    date = models.DateField(blank=False, null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)
    interviewer_time_slot = models.ForeignKey(InterviewerFreeTime, default=False)
    buffer_time = models.BooleanField(default=False)

    has_confirmed = models.BooleanField(default=False)
    has_received_email = models.BooleanField(default=False)

    objects = InterviewQuerySet.as_manager()
