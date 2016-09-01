from django.db import models
from django.utils import timezone

from loki.education.models import Course
from loki.base_app.models import BaseUser


class ApplicationInfo(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    course = models.OneToOneField(Course)

    def __str__(self):
        return "From {0} to {1} applying to {2}".format(self.start_date,
                                                        self.end_date,
                                                        self.course)

    def apply_is_active(self):
        return self.end_date >= timezone.now()

class ApplicationProblem(models.Model):
    application_info = models.ManyToManyField(ApplicationInfo)
    name = models.CharField(max_length=30)
    description_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Application(models.Model):
    application_info = models.ForeignKey(ApplicationInfo)
    user = models.ForeignKey(BaseUser)

    phone = models.CharField(null=True, blank=True, max_length=20)
    skype = models.CharField(null=True, blank=True, max_length=30)
    works_at = models.CharField(null=True, blank=True, max_length=110)
    studies_at = models.CharField(blank=True, null=True, max_length=110)

    def __str__(self):
        return "{0} to {1}".format(self.user, self.application_info)

    class Meta:
        unique_together = (("application_info", "user"),)


class ApplicationProblemSolution(models.Model):
    application = models.ForeignKey(Application)
    problem = models.OneToOneField(ApplicationProblem)
    solution_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{0} to {1}".format(self.problem, self.application)
