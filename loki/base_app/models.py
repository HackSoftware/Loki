from loki.local_settings import MEDIA_ROOT
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.URLField(blank=True)
    jobs_link = models.URLField(blank=True)

    def get_logo(self):
        if self.logo:
            return MEDIA_ROOT + 'logos/' + str(self.pk) + '.JPG'