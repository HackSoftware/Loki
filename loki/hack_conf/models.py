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

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    picture = models.ImageField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    day = models.SmallIntegerField()
    name = models.CharField(max_length=150)
    time = models.TimeField()
    description = models.TextField(blank=True)
    author = models.ForeignKey(Speaker)

