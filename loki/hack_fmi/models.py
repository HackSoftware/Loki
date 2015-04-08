from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from ckeditor.fields import RichTextField


class UserManager(BaseUserManager):

    def __create_user(self, email, password, is_admin, is_active,
                      full_name):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_admin=is_admin,
                          is_active=is_active,
                          full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name=''):
        return self.__create_user(email, password, False, False,
                                  full_name)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, True, True, full_name)


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


class TeamMembership(models.Model):
    competitor = models.ForeignKey('Competitor')
    team = models.ForeignKey('Team')
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".foramt(self.competitor, self.team)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(Competitor, through='TeamMembership')
    idea_description = models.TextField()
    repository = models.URLField(blank=True)
    technologies = models.ManyToManyField(Skill)
    season = models.ForeignKey('Season', default=1)

    def add_member(self, competitor, is_leader=False):
        return TeamMembership.objects.create(
            competitor=competitor,
            team=self,
            is_leader=is_leader
        )

    def get_leader(self):
        for membership in self.teammembership_set.all():
            if membership.is_leader:
                return membership.competitor

    def __str__(self):
        return self.name


class Season(models.Model):
    number = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            try:
                currently_active = self.__class__.objects.get(is_active=True)
            except self.__class__.DoesNotExist:
                pass
            else:
                currently_active.is_active = False
                currently_active.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.number


class Invitation(models.Model):
    team = models.ForeignKey(Team)
    competitor = models.ForeignKey(Competitor)

    class Meta:
        unique_together = ('team', 'competitor')

    def __str__(self):
        return "{} {}".foramt(self.team, self.competitor)


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    picture = models.ImageField(blank=True)

    def __str__(self):
        return self.name
