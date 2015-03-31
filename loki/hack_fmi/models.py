from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def __create_user(self, email, password, is_admin,
                      full_name):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_admin=is_admin,
                          full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name=''):
        return self.__create_user(email, password, False,
                                  full_name)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, full_name, True)


class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @full_name.setter
    def full_name(self, full_name):
        names = full_name.strip().split()
        if len(names) >= 2:
            self.first_name = names[0]
            self.last_name = names[-1]
        else:
            raise ValueError('Not valid full_name.')

    def get_competitor(self):
        try:
            return self.competitor
        except:
            return False


class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Competitor(BaseUser):
    S = 1
    M = 2
    L = 3
    XL = 4

    SHIRT_SIZE = (
        (S, 'S'),
        (M, 'M'),
        (L, 'L'),
        (XL, 'XL')
    )

    is_vegetarian = models.BooleanField(default=False)
    known_skills = models.ManyToManyField(Skill)
    faculty_number = models.IntegerField()
    shirt_size = models.SmallIntegerField(choices=SHIRT_SIZE, default=S)
    needs_work = models.BooleanField(default=True)
    social_links = models.TextField(blank=True)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(Competitor, through='TeamMembership')
    idea_description = models.TextField()
    repository = models.URLField(blank=True)
    technologies = models.ManyToManyField(Skill)
    season = models.ForeignKey('Season', default=0)


class TeamMembership(models.Model):
    competitor = models.ForeignKey(Competitor)
    team = models.ForeignKey(Team)
    is_leader = models.BooleanField(default=False)


class Season(models.Model):
    number = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=False)
