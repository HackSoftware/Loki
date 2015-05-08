from django.db import models


class HackConfUser(models.Model):
    email = models.EmailField(unique=True)
    datetime = models.DateTimeField(auto_now=True)


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    facebook = models.URLField()
    twitter = models.URLField()
    google_plus = models.URLField()
    github = models.URLField()
