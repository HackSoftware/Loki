import requests
from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField
from base_app.models import City, Company

from hack_fmi.models import BaseUser
from .validators import validate_mac


class Student(BaseUser):
    courses = models.ManyToManyField('Course', through='CourseAssignment')
    mac = models.CharField(validators=[validate_mac], max_length=17, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=20)
    skype = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return self.full_name


class Teacher(BaseUser):
    mac = models.CharField(validators=[validate_mac], max_length=17, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=20)
    teached_courses = models.ManyToManyField('Course')


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
    student_presence = models.PositiveSmallIntegerField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')


class Course(models.Model):
    # TODO:
    # Moved to website.models.CourseDescription
    # Delete (comment) the fields after you migrade the info too!
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
    fb_group = models.URLField(blank=True, null=True)
    next_season_mail_list = models.URLField(null=True, blank=True)
    SEO_description = models.CharField(blank=False, max_length=255)
    SEO_title = models.CharField(blank=False, max_length=255)
    start_time = models.DateField(blank=True, null=True)
    url = models.SlugField(max_length=80, unique=True)
    video = models.URLField(blank=True)
    generate_certificates_until = models.DateField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class CheckIn(models.Model):
    mac = models.CharField(max_length=17)
    student = models.ForeignKey('Student', null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (('student', 'date'), ('mac', 'date'))


class Lecture(models.Model):
    course = models.ForeignKey('Course')
    date = models.DateField()


class StudentNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Teacher)
    post_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('post_time',)


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=110)

    def __str__(self):
        return self.name


class Task(models.Model):
    course = models.ForeignKey(Course)
    description = models.URLField()
    is_exam = models.BooleanField(default=False)
    name = models.CharField(max_length=128)
    week = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'description'),)


class Test(models.Model):
    UNITTEST = 0

    TYPE_CHOICE = (
        (UNITTEST, 'unittest'),
    )

    task = models.OneToOneField(Task)
    language = models.ForeignKey(ProgrammingLanguage)
    code = models.TextField(blank=True, null=True)
    github_url = models.URLField()
    test_type = models.SmallIntegerField(choices=TYPE_CHOICE, default=UNITTEST)

    def __str__(self):
        return "{}/{}".format(self.task, self.language)


class Solution(models.Model):
    PENDING = 0
    RUNNING = 1
    OK = 2
    NOT_OK = 3

    STATUS_CHOICE = (
        (PENDING, 'pending'),
        (RUNNING, 'running'),
        (OK, 'ok'),
        (NOT_OK, 'not_ok'),
    )

    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    url = models.URLField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    build_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=PENDING)

    def update_status(self):
        address = settings.GRADER_ADDRESS
        url = address + 'check_result/{}/'.format(self.build_id)
        r = requests.get(url)

        if r.status_code == 204:
            self.status = Solution.PENDING
        elif r.status_code == 200 and r.json()['result_status'] == 'ok':
            self.status = Solution.OK
        elif r.status_code == 200 and r.json()['result_status'] == 'not_ok':
            self.status = Solution.NOT_OK
        self.save()

        return Solution.STATUS_CHOICE[self.status][1]

    def get_assignment(self):
        return CourseAssignment.objects.get(user=self.student, course=self.task.course)


class GraderRequest(models.Model):
    request_info = models.CharField(max_length=140)
    nonce = models.BigIntegerField(db_index=True)


class WorkingAt(models.Model):
    student = models.ForeignKey(Student)
    company = models.ForeignKey(Company, blank=True, null=True)
    location = models.ForeignKey(City)
    course = models.ForeignKey(Course, blank=True, null=True)

    came_working = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class Certificate(models.Model):
    assignment = models.OneToOneField(CourseAssignment)
