from django.db import models


class HackConfUser(models.Model):
    email = models.EmailField(unique=True)
    datetime = models.DateTimeField(auto_now=True)
