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


class Partner(models.Model):
    description = RichTextField(blank=False)
    facebook = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    logo = models.ImageField(upload_to="partner_logoes", null=True, blank=True)
    money_spent = models.PositiveIntegerField(default=0, blank=False, null=False)
    name = models.CharField(max_length=128)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.name
