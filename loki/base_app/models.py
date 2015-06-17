from loki.settings import MEDIA_ROOT
from django.db import models

from ckeditor.fields import RichTextField


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.URLField(blank=True)
    jobs_link = models.URLField(blank=True)

    def get_logo(self):
        if self.logo:
            return MEDIA_ROOT + 'logos/' + str(self.pk) + '.JPG'

    def __str__(self):
        return self.name


class Partner(models.Model):
    comapny = models.OneToOneField(Company, primary_key=True)
    description = RichTextField(blank=False)
    facebook = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    money_spent = models.PositiveIntegerField(default=0, blank=False, null=False)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.comapny.name


class Event(models.Model):
    name = models.CharField(max_length=150)
    start_date = models.DateField()
    url = models.URLField()


class Ticket(models.Model):
    event = models.ForeignKey('Event')
    base_user = models.ForeignKey('hack_fmi.BaseUser')

    class Meta:
        unique_together = ('event', 'base_user')
