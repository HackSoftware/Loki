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
    title = models.CharField(blank=True, max_length=255)
    url = models.SlugField(max_length=80, unique=True)
    video_image = models.ImageField(blank=True)

    # There are such fields in Course:
    # video_url = models.URLField(blank=True)
    # video_url = Course.video
    # start_time = Course.start_time
    # end_time = Course.end_time

    # Is this a number or percentage??????????
    # course_intensity = models.IntegerField(max_digits=8, default=0)
    # course_days = ? each day as a field (true/false)??

    # There is such field in Course - Course.application_until
    # application_deadline = models.DateField(blank=True, null=True)

    # Theere is such field in Course - Course.git_repository
    # github = models.URLField(blank=True, null=True)
    course_summary = RichTextField(blank=True, null=True)

    # teachers = Course.teachers_set
    realization = RichTextField(blank=True, null=True)
    # partners = Course.partner_set

    price = RichTextField(blank=True, null=True)

    # Do we need these fields
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)
