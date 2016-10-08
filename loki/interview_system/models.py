import uuid
from django.db import models

from loki.base_app.models import BaseUser
from loki.applications.models import ApplicationInfo, Application

from .query import InterviewQuerySet
from .managers import InterviewerManager


class Interviewer(BaseUser):
    courses_to_interview = models.ManyToManyField(ApplicationInfo)
    interviews = models.ManyToManyField(Application, through='Interview')
    skype = models.CharField(null=True, blank=True, max_length=30)

    objects = InterviewerManager()


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
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    interviewer_comment = models.TextField(null=True, blank=True,
                                           help_text='Коментар от интервюиращия')
    possible_ratings = [(i, i) for i in range(11)]
    code_skills_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка върху уменията на кандидата да пише'
        ' код и върху знанията му за базови алгоритми')
    code_design_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка върху уменията на кандидата да "съставя'
        ' програми", да разбива нещата на парчета + базово OOP')
    fit_attitude_rating = models.IntegerField(
        default=0,
        choices=possible_ratings,
        help_text='Оценка на интервюиращия в зависимост от'
        ' усета му за човека (подходящ ли е за курса)')

    has_confirmed = models.BooleanField(default=False)
    has_received_email = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    objects = InterviewQuerySet.as_manager()

    def reset(self):
        self.application = None
        self.has_received_email = False
        self.has_confirmed = False

        self.save()
