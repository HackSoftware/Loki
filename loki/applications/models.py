from django.db import models

from .education import Course
from .base_app import BaseUser

# Create your models here.
class ApplyCourse(models.Model):
    pass
    # fk Course
    # fk BaseUser (OneToOneField)

    # phone = models.CharField(null=True, blank=True, max_length=20)
    # skype = models.CharField(null=True, blank=True)
    #
    # working_at = models.CharField()
    # study_at = models.CharField()
    #
    # tasks = []
