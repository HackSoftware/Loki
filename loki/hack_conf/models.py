from django.db import models


class HackConfUser(models.Model):
    email = models.EmailField(unique=True)
    datetime = models.DateTimeField(auto_now=True)


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
    github = models.URLField(blank=True)


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    picture = models.ImageField()
