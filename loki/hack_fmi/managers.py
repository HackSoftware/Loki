from django.db import models

from .query import TeamMembershipQuerySet


class TeamMembershipManager(models.Manager):

    def get_queryset(self):
        return TeamMembershipQuerySet(self.model, using=self._db)

    def list_all_teams_for_competitor(self, competitor):
        qs = self.get_queryset().get_all_team_memberships_for_competitor(competitor=competitor)
        return [team_membership.team for team_membership in qs]

    def get_leader_of_team(self, team):
        return self.get_queryset().get_team_membership_of_leader(team=team).first().team.get_leader()
