from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from ckeditor.fields import RichTextField
from django_resized import ResizedImageField


class UserManager(BaseUserManager):

    def __create_user(self, email, password, is_staff, is_active, full_name, is_superuser):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          full_name=full_name,
                          is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name=''):
        return self.__create_user(email, password, False, False,
                                  full_name, False)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, True, True, full_name, True)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    avatar = ResizedImageField(
        upload_to='avatar',
        size=[300, 200],
        blank=True,
    )

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

    def make_competitor(self):
        competitor = Competitor(baseuser_ptr_id=self.id)
        competitor.save()
        competitor.__dict__.update(self.__dict__)
        return competitor.save()


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
    faculty_number = models.IntegerField(null=True)
    shirt_size = models.SmallIntegerField(choices=SHIRT_SIZE, default=S)
    needs_work = models.BooleanField(default=True)
    social_links = models.TextField(blank=True)
    registered = models.BooleanField(default=False)


class TeamMembership(models.Model):
    competitor = models.ForeignKey('Competitor')
    team = models.ForeignKey('Team')
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.competitor, self.team)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('Competitor', through='TeamMembership')
    mentors = models.ManyToManyField('Mentor', blank=True)
    technologies = models.ManyToManyField('Skill', blank=True)
    idea_description = models.TextField()
    repository = models.URLField(blank=True)
    season = models.ForeignKey('Season', default=1)
    need_more_members = models.BooleanField(default=True)
    members_needed_desc = models.CharField(max_length=255, blank=True)
    room = models.ForeignKey('Room', null=True, blank=True)
    picture = models.ImageField(blank=True)
    place = models.SmallIntegerField(null=True)

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
    name = models.CharField(max_length=100, null=True)
    topic = models.CharField(max_length=100)
    front_page = RichTextField(blank=True)
    min_team_members_count = models.SmallIntegerField(default=1)
    max_team_members_count = models.SmallIntegerField(default=6)
    sign_up_deadline = models.DateField()
    make_team_dead_line = models.DateField()
    mentor_pick_start_date = models.DateField()
    mentor_pick_end_date = models.DateField()
    max_mentor_pick = models.SmallIntegerField(default=1)
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
        return self.name


class Invitation(models.Model):
    team = models.ForeignKey(Team)
    competitor = models.ForeignKey(Competitor)

    class Meta:
        unique_together = ('team', 'competitor')

    def __str__(self):
        return "{} {}".format(self.team, self.competitor)


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    picture = models.ImageField(blank=True)
    seasons = models.ManyToManyField('Season')
    from_company = models.ForeignKey('Partner', null=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('order',)


class Room(models.Model):
    number = models.IntegerField()
    season = models.ForeignKey(Season)
    capacity = models.SmallIntegerField()

    def get_number_of_teams(self):
        return len(self.team_set.all())

    def is_full(self):
        return len(self.team_set.all()) >= self.capacity

    def __str__(self):
        return str(self.number)


class Partner(models.Model):
    name = models.CharField(max_length=60)
    seasons = models.ManyToManyField('Season')

    def __str__(self):
        return self.name
