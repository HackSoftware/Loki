from django.db import models
from django.utils import timezone

from loki.website.models import CourseDescription
from loki.base_app.models import BaseUser

from ckeditor.fields import RichTextField

from .managers import ApplicationInfoManager
from .query import ApplicationQuerySet


class ApplicationInfo(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    course = models.OneToOneField(CourseDescription)
    start_interview_date = models.DateTimeField(blank=False, null=True)
    end_interview_date = models.DateTimeField(blank=False, null=True)

    description = RichTextField(
        blank=True,
        null=True,
        help_text='Това описва процедурата по кандидатстване. Излиза тук /apply/edit/<course-url>'
    )

    external_application_form = models.URLField(blank=True, null=True,
                                                help_text='Only add if course requires external application form')

    objects = ApplicationInfoManager()

    def __str__(self):
        return "From {0} to {1} applying to {2}".format(self.start_date,
                                                        self.end_date,
                                                        self.course)

    def apply_is_active(self):
        return self.end_date >= timezone.now()

    def interview_is_active(self):
        return self.start_interview_date <= timezone.now() and \
               self.end_interview_date >= timezone.now()


class ApplicationProblem(models.Model):
    application_info = models.ManyToManyField(ApplicationInfo)
    name = models.CharField(max_length=255)
    description_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Application(models.Model):
    application_info = models.ForeignKey(ApplicationInfo)
    user = models.ForeignKey(BaseUser)

    phone = models.CharField(null=True, blank=True, max_length=255)
    skype = models.CharField(null=True, blank=True, max_length=255)
    works_at = models.CharField(null=True, blank=True, max_length=255)
    studies_at = models.CharField(blank=True, null=True, max_length=255)
    has_interview_date = models.BooleanField(default=False)

    objects = ApplicationQuerySet.as_manager()

    def __str__(self):
        return "{0} to {1}".format(self.user, self.application_info)

    class Meta:
        unique_together = (("application_info", "user"),)


class ApplicationProblemSolution(models.Model):
    application = models.ForeignKey(Application)
    problem = models.ForeignKey(ApplicationProblem)
    solution_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{0} to {1}".format(self.problem, self.application)
