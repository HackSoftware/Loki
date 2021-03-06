from django.db import models

from ckeditor.fields import RichTextField

from loki.education.models import Course


class SuccessStoryPerson(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(blank=True)
    show_picture_on_site = models.BooleanField(default=True)
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

    custom_logo = models.ImageField(
        blank=True,
        help_text='Add a custom course logo with 308x308 size.')
    url = models.SlugField(max_length=80, unique=True)

    video_image = models.ImageField(
        blank=True,
        help_text='Add a 16/9 video cover image.')
    video = models.URLField(blank=True)

    blog_article = models.CharField(
        blank=True,
        max_length=255)
    course_intensity = models.PositiveIntegerField(default=0, blank=False, null=False)
    course_days = models.CharField(blank=True, max_length=255)
    paid_course = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)

    course_summary = RichTextField(blank=True, null=True)
    teacher_preview = RichTextField(blank=True, null=True)
    realization = RichTextField(blank=True, null=True)
    price_text = RichTextField(blank=True, null=True)
    list_courses_text = RichTextField(
        blank=True,
        null=True,
        help_text='Това е малък текст за /courses страницата'
    )
    address = models.CharField(
        blank=True,
        max_length=255,
        help_text='Add <a href="http://www.google.com/maps" target="_blank">google maps</a>'
        ' link to HackBulgaria location')
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.course.name
