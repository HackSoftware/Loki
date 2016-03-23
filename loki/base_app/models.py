from django.db import models
from loki.settings import MEDIA_ROOT

from ckeditor.fields import RichTextField


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="partners_logoes", null=True, blank=True)
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

    video_presentation = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.comapny.name


class GeneralPartner(models.Model):
    partner = models.OneToOneField(Partner, primary_key=True)

    def __str__(self):
        return self.partner.comapny.name


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
