from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from loki.settings import MEDIA_ROOT

from ckeditor.fields import RichTextField


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="partners_logoes", null=True, blank=True)
    jobs_link = models.URLField(blank=True)

    def get_logo(self):
        if self.logo:
            return MEDIA_ROOT + 'logos/' + str(self.pk) + '.JPG'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Partner(models.Model):
    comapny = models.OneToOneField(Company, primary_key=True)
    description = RichTextField(blank=False)
    facebook = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    money_spent = models.PositiveIntegerField(default=0, blank=False, null=False)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    video_presentation = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.comapny.name


class GeneralPartner(models.Model):
    partner = models.OneToOneField(Partner, primary_key=True)

    def __str__(self):
        return self.partner.comapny.name


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class EducationPlace(models.Model):
    name = models.CharField(max_length=1000)
    city = models.ForeignKey(City)

    def is_uni(self):
        return hasattr(self, 'university')

    def is_school(self):
        return hasattr(self, 'school')

    def is_academy(self):
        return hasattr(self, 'academy')

    def __str__(self):
        return "{} ({})".format(self.name, self.city)

    class Meta:
        unique_together = (('name', 'city'),)


class University(EducationPlace):
    class Meta:
        verbose_name_plural = 'Universities'


class Faculty(models.Model):
    uni = models.ForeignKey(University)
    name = models.CharField(max_length=1000)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, str(self.uni))

    class Meta:
        unique_together = (('uni', 'name'),)
        verbose_name_plural = 'Faculties'


class Subject(models.Model):
    faculty = models.ForeignKey(Faculty)
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return "{} - {}".format(self.name, str(self.faculty))

    class Meta:
        unique_together = (('faculty', 'name'),)


class School(EducationPlace):
    pass


class Academy(EducationPlace):
    pass


class UserManager(BaseUserManager):

    def __create_user(self, email, password, full_name,
                      is_staff=False, is_active=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          full_name=full_name,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name='', **kwargs):
        return self.__create_user(email, password, full_name, is_staff=False, is_active=False,
                                  is_superuser=False, **kwargs)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, full_name, is_staff=True,
                                  is_active=True, is_superuser=True)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    birth_place = models.ForeignKey(City, null=True, blank=True)

    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    twitter_account = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    studies_at = models.CharField(blank=True, null=True, max_length=110)
    works_at = models.CharField(null=True, blank=True, max_length=110)

    avatar = models.ImageField(blank=True, null=True)
    full_image = models.ImageField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_competitor(self):
        try:
            return self.competitor
        except:
            return False

    def get_student(self):
        try:
            return self.student
        except:
            return False

    def get_teacher(self):
        try:
            return self.teacher
        except:
            return False

    def make_competitor(self):
        competitor = Competitor(baseuser_ptr_id=self.id)
        competitor.save()
        competitor.__dict__.update(self.__dict__)
        return competitor.save()
