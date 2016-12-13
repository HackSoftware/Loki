from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from loki.base_app.models import BaseUser

from .query import (TeamQuerySet, TeamMembershipQuerySet,
                    TeamMentorshipQuerySet, CompetitorQuerySet,
                    InvitationQuerySet)
from .managers import TeamMembershipManager


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
    other_skills = models.CharField(max_length=255, blank=True, default='')
    faculty_number = models.IntegerField(null=True)
    shirt_size = models.SmallIntegerField(choices=SHIRT_SIZE, default=S)
    needs_work = models.BooleanField(default=True)
    social_links = models.TextField(blank=True)
    registered = models.BooleanField(default=False)

    objects = CompetitorQuerySet.as_manager()


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


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('Competitor', through='TeamMembership')
    mentors = models.ManyToManyField('Mentor', through='TeamMentorship')
    technologies = models.ManyToManyField('Skill', blank=True)
    idea_description = models.TextField()
    repository = models.URLField(blank=True)
    season = models.ForeignKey('Season')
    need_more_members = models.BooleanField(default=True)
    members_needed_desc = models.CharField(max_length=255, blank=True)
    room = models.ForeignKey('Room', null=True, blank=True)
    updated_room = models.CharField(max_length=100, null=True, blank=True)
    place = models.SmallIntegerField(blank=True, null=True)

    objects = TeamQuerySet.as_manager()

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

    class Meta:
        unique_together = (('name', 'season'),)


class TeamMentorship(models.Model):
    mentor = models.ForeignKey(Mentor)
    team = models.ForeignKey(Team)

    objects = TeamMentorshipQuerySet.as_manager()

    class Meta:
        unique_together = ('mentor', 'team')

    def clean(self):
        """
        TODO: Take in mind the season max_mentor_count
        """


class TeamMembership(models.Model):
    competitor = models.ForeignKey('Competitor')
    team = models.ForeignKey('Team')
    is_leader = models.BooleanField(default=False)

    objects = TeamMembershipManager.from_queryset(TeamMembershipQuerySet)()

    def __str__(self):
        return "{} {}".format(self.competitor, self.team)


class Invitation(models.Model):
    team = models.ForeignKey(Team)
    competitor = models.ForeignKey(Competitor)

    objects = InvitationQuerySet.as_manager()

    class Meta:
        unique_together = ('team', 'competitor')

    def __str__(self):
        return "{} {}".format(self.team, self.competitor)


class SeasonCompetitorInfo(models.Model):
    competitor = models.ForeignKey(Competitor)
    season = models.ForeignKey(Season)
    looking_for_team = models.BooleanField(default=False)

    class Meta:
        unique_together = ('competitor', 'season')


class BlackListToken(models.Model):
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
