import uuid
from dateutil import rrule

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from jsonfield import JSONField

from loki.base_app.models import BaseUser, City, Company

from .validators import validate_mac
from .exceptions import HasToBeRetested
from .query import (CheckInQuerySet, CourseQuerySet, TaskQuerySet,
                    SolutionQuerySet)


class StudentAndTeacherCommonModel(models.Model):
    mac = models.CharField(validators=[validate_mac], max_length=17, blank=True, null=True)
    phone = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        abstract = True


class Student(BaseUser, StudentAndTeacherCommonModel):
    courses = models.ManyToManyField('Course', through='CourseAssignment')
    skype = models.CharField(null=True, blank=True, max_length=20)
    looking_for_job = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    def get_english_names(self):
        return self.english_names


class Teacher(BaseUser, StudentAndTeacherCommonModel):
    signature = models.ImageField(upload_to="teachers_signatures", null=True, blank=True)
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
    favourite_partners = models.ManyToManyField('base_app.Partner', blank=True)
    group_time = models.SmallIntegerField(choices=GROUP_TIME_CHOICES)
    is_attending = models.BooleanField(default=True)
    user = models.ForeignKey('Student')
    student_presence = models.PositiveSmallIntegerField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name,
                                   self.user.last_name,
                                   self.course)


class Course(models.Model):
    name = models.CharField(blank=False, max_length=64, unique=True)

    git_repository = models.CharField(blank=True, max_length=256)
    fb_group = models.URLField(blank=True, null=True)
    video_channel = models.URLField(blank=True, null=True)

    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    deadline_date = models.DateField(blank=True, null=True)
    generate_certificates_until = models.DateField()
    english_name = models.CharField(null=True, blank=True, max_length=50)

    partner = models.ManyToManyField('base_app.Partner', blank=True)

    objects = CourseQuerySet.as_manager()

    def is_active(self):
        return self.end_time >= timezone.now().date()

    def is_in_deadline(self):
        if self.deadline_date:
            return self.deadline_date >= timezone.now().date()

        return self.is_active()

    def get_english_name(self):
        return self.english_name

    @property
    def duration_in_weeks(self):
        weeks = rrule.rrule(
            rrule.WEEKLY,
            dtstart=self.start_time,
            until=self.end_time
        )
        return weeks.count()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class CheckIn(models.Model):
    mac = models.CharField(max_length=17)
    user = models.ForeignKey(BaseUser, null=True, blank=True, related_name='checkins')
    date = models.DateField(auto_now_add=True)

    objects = CheckInQuerySet.as_manager()

    class Meta:
        unique_together = (('user', 'date'), ('mac', 'date'))


class Week(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return "Week{0}".format(self.number)


class Lecture(models.Model):
    course = models.ForeignKey('Course')
    date = models.DateField()
    week = models.ForeignKey(Week, null=True, blank=True)
    presentation_url = models.URLField(blank=True, null=True)

    def is_date_in_future(self):
        return self.date > timezone.now().date()


class StudentNote(models.Model):
    text = models.TextField(blank=True)
    assignment = models.ForeignKey(CourseAssignment)
    author = models.ForeignKey(Teacher)
    post_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('post_time',)

    def __str__(self):
        return "{}".format(self.assignment.user)


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
    gradable = models.BooleanField(default=True)

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return self.name

    def has_tests(self):
        return getattr(self, 'test', None) is not None

    class Meta:
        unique_together = (('name', 'description'),)


class RetestSolution(models.Model):
    PENDING = 0
    DONE = 1

    STATUS_CHOICE = (
        (PENDING, 'pending'),
        (DONE, 'done'),
    )

    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=PENDING)
    date = models.DateTimeField(auto_now_add=True)
    test_id = models.IntegerField()
    tested_solutions_count = models.IntegerField(default=0)


class Test(models.Model):
    UNITTEST = 0

    TYPE_CHOICE = (
        (UNITTEST, 'unittest'),
    )

    task = models.OneToOneField(Task)
    language = models.ForeignKey(ProgrammingLanguage)
    test_type = models.SmallIntegerField(choices=TYPE_CHOICE, default=UNITTEST)
    extra_options = JSONField(blank=True, null=True)

    @property
    def options(self):
        if self.extra_options is None:
            return {}

        return self.extra_options

    def __str__(self):
        return "{}/{}".format(self.task, self.language)

    # Check if test code is changed. If yes - retest solutions (i refuse to use flags)
    def save(self, *args, **kwargs):

        if self.id is not None:
            old_test = Test.objects.get(id=self.id)

            try:
                if bool(old_test.is_binary()) != bool(self.is_binary()):
                    raise HasToBeRetested

                if self.is_binary():
                    if self.binaryfiletest.file.name != old_test.binaryfiletest.file.name:
                        raise HasToBeRetested

                if self.is_source():
                    if self.sourcecodetest.code != old_test.sourcecodetest.code:
                        raise HasToBeRetested

            except HasToBeRetested:
                RetestSolution.objects.create(test_id=self.id)

        return super().save(*args, **kwargs)

    def is_binary(self):
        if hasattr(self, 'binaryfiletest'):
            return True

        return False

    def is_source(self):
        if hasattr(self, 'sourcecodetest'):
            return True

        return False

    def test_mode(self):
        if self.is_binary():
            return "binary"

        return "source"


class SourceCodeTest(Test):
    code = models.TextField(blank=True, null=True)


class BinaryFileTest(Test):
    file = models.FileField(upload_to="tests")


class Solution(models.Model):
    PENDING = 0
    RUNNING = 1
    OK = 2
    NOT_OK = 3
    SUBMITED = 4
    MISSING = 5
    SUBMITTED_WITHOUT_GRADING = 6

    STATUS_CHOICE = (
        (PENDING, 'pending'),
        (RUNNING, 'running'),
        (OK, 'ok'),
        (NOT_OK, 'not_ok'),
        (SUBMITED, 'submitted'),
        (MISSING, 'missing'),
        (SUBMITTED_WITHOUT_GRADING, 'submitted_without_grading'),
    )

    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    url = models.URLField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    build_id = models.IntegerField(blank=True, null=True)
    check_status_location = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=SUBMITTED_WITHOUT_GRADING)
    test_output = models.TextField(blank=True, null=True)
    return_code = models.IntegerField(blank=True, null=True)
    file = models.FileField(upload_to="solutions", blank=True, null=True)

    def get_status(self):
        try:
            status = Solution.STATUS_CHOICE[self.status][1]
        except:
            status = Solution.STATUS_CHOICE[Solution.MISSING][1]
        return status

    objects = SolutionQuerySet.as_manager()


class GraderRequest(models.Model):
    request_info = models.CharField(max_length=140)
    nonce = models.BigIntegerField(db_index=True)


class WorkingAt(models.Model):
    student = models.ForeignKey(Student)
    company = models.ForeignKey(Company, blank=True, null=True)
    location = models.ForeignKey(City, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)

    came_working = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} from {}".format(self.company_name, self.start_date)

    def __repr__(self):
        return self.__str__()

    def clean(self):
        if self.company and self.company_name:
            self.company_name = None

        if not self.company and not self.company_name:
            raise ValidationError({'company': ['Това поле е задължително.']})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Certificate(models.Model):
    assignment = models.OneToOneField(CourseAssignment)
    token = models.CharField(default=uuid.uuid4, unique=True, max_length=110)


class Material(models.Model):
    course = models.ForeignKey('Course')
    week = models.ForeignKey(Week, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
