from django.db import models

from education.models import Course
from base_app.models import BaseUser

# Create your models here.
class ApplyCourse(models.Model):
    user = models.OneToOneField(BaseUser, primary_key=True)
    course = models.OneToOneField(Course)

    phone = models.CharField(null=True, blank=True, max_length=20)
    skype = models.CharField(null=True, blank=True, max_length=30)

    works_at = models.CharField(null=True, blank=True, max_length=110)
    studies_at = models.CharField(blank=True, null=True, max_length=110)
    # task1 = models.URLField(blank=True, null=True)
    # task2 = models.URLField(blank=True, null=True)
    # task3 = models.URLField(blank=True, null=True)
    # task4 = models.URLField(blank=True, null=True)
    # task5 = models.URLField(blank=True, null=True)

    def __str__(self):
        return "{0} applies to {1}".format(self.user, self.course)
