from django.db import models
from education.models import Course

from ckeditor.fields import RichTextField


class SuccessStoryPerson(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __str__(self):
        return self.name


class SuccessVideo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    youtube_link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    label = models.CharField(max_length=80, unique=True)
    text = RichTextField(blank=True)

    def __str__(self):
        return self.label


class CourseDescription(models.Model):
    course = models.OneToOneField(Course)
    url = models.SlugField(max_length=80, unique=True)
    video_image = models.ImageField(blank=True)
    course_intensity = models.PositiveIntegerField(default=0, blank=False, null=False)
    course_days = models.CharField(blank=True, max_length=255)
    course_summary = RichTextField(blank=True, null=True)
    realization = RichTextField(blank=True, null=True)
    price = RichTextField(blank=True, null=True)
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)
    # title = Course.name
    # video_url = Course.video
    # start_time = Course.start_time
    # end_time = Course.end_time
    # application_deadline = Course.application_until
    # github = Course.git_repository
    # teachers = Course.teachers_set
    # partners = Course.partner_set

    def __str__(self):
        return self.title
