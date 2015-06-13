from django.db import models

from ckeditor.fields import RichTextField

from hack_fmi.models import BaseUser
from .validators import validate_mac


class Student(BaseUser):
    STUDENT = 1
    HR = 2
    TEACHER = 3

    STATUSES = (
        (STUDENT, 'Student'),
        (HR, 'HR'),
        (TEACHER, 'Teacher'),
    )

    status = models.SmallIntegerField(choices=STATUSES, default=STUDENT)
    courses = models.ManyToManyField('Course', through='CourseAssignment')
    hr_of = models.ForeignKey('base_app.Partner', blank=True, null=True)
    mac = models.CharField(validators=[validate_mac], max_length=17, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length='20')


class Teacher(BaseUser):
    mac = models.CharField(validators=[validate_mac], max_length=17, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length='20')
    teached_courses = models.ManyToManyField('Course')


class HR(BaseUser):
    phone = models.CharField(null=True, blank=True, max_length='20')
    teached_courses = models.ManyToManyField('Course')
    company = models.ForeignKey('base_app.Partner')


class CourseAssignment(models.Model):
    EARLY = 1
    LATE = 2

    GROUP_TIME_CHOICES = (
        (EARLY, 'Early'),
        (LATE, 'Late'),
    )

    course = models.ForeignKey('Course')
    cv = models.FileField(blank=True, null=True, upload_to='cvs')
    favourite_partners = models.ManyToManyField('base_app.Partner', null=True, blank=True)
    group_time = models.SmallIntegerField(choices=GROUP_TIME_CHOICES)
    is_attending = models.BooleanField(default=True)
    user = models.ForeignKey('Student')
    is_online = models.BooleanField(default=False)


class Course(models.Model):
    description = RichTextField(blank=False)
    git_repository = models.CharField(blank=True, max_length=256)
    image = models.ImageField(upload_to="courses_logoes", null=True, blank=True)
    name = models.CharField(blank=False, max_length=64)
    partner = models.ManyToManyField('base_app.Partner', null=True, blank=True)
    short_description = models.CharField(blank=True, max_length=300)
    show_on_index = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)

    application_until = models.DateField()
    applications_url = models.URLField(null=True, blank=True)
    ask_for_favorite_partner = models.BooleanField(default=False)
    ask_for_feedback = models.BooleanField(default=False)
    end_time = models.DateField(blank=True, null=True)
    next_season_mail_list = models.URLField(null=True, blank=True)
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)
    start_time = models.DateField(blank=True, null=True)
    url = models.SlugField(max_length=80, unique=True)
    video = models.URLField(blank=True)

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    mac = models.CharField(max_length=17)
    student = models.ForeignKey('Student', null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('student', 'date'), ('mac', 'date'))


class Lecture(models.Model):
    course = models.ForeignKey('Course')
    date = models.DateField()


class StudentNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Teacher)
    post_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('post_time',)
