from django.db import models


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
    github = models.URLField(blank=True)
    video_presentation = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Sponsor(models.Model):

    SPONSOR = 1
    GENERAL_MEDIA_PARTNER = 2
    BRANCH_PARTNER = 3
    MEDIA_PARTNER = 4
    SCHOOL_PARTNER = 5
    SPONSOR_SILVER = 6
    SPONSOR_GOLD = 7
    SPONSOR_PLATINUM = 8

    TITLE_TYPE = (
        (SPONSOR, 'Sponsor'),
        (GENERAL_MEDIA_PARTNER, 'General Media Partner'),
        (BRANCH_PARTNER, 'Branch Partner'),
        (MEDIA_PARTNER, 'Media Partner'),
        (SCHOOL_PARTNER, 'School Partner'),
        (SPONSOR_SILVER, 'Silver Sponsor'),
        (SPONSOR_GOLD, 'Gold Sponsor'),
        (SPONSOR_PLATINUM, 'Platinum Sponsor'),

    )
    title = models.SmallIntegerField(choices=TITLE_TYPE, default=SPONSOR)
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
