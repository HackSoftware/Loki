from django.db import models

from .query import TeamMembershipQuerySet


class TeamMembershipManager(models.Manager):

    def get_queryset(self):
        return TeamMembershipQuerySet(self.model, using=self._db)

    def list_all_teams_for_competitor(self, competitor):
        qs = self.get_queryset().get_all_team_memberships_for_competitor(competitor=competitor)
        return [team_membership.team for team_membership in qs]

    # TODO: watch out when get_team_membership_of_leader returns [] -> .first()
    def get_leader_of_team(self, team):
        try:
            return self.get_queryset().get_team_membership_of_leader(team=team).first().team.get_leader()
        except AttributeError:  # Team has no leader
            return None

    def is_competitor_leader_of_team(self, competitor, team):
        return self.get_queryset().get_all_team_memberships_for_competitor(competitor=competitor).\
            get_team_membership_of_leader(team=team).exists()

    def is_competitor_leader(self, competitor):
        return self.get_queryset().get_team_membership_for_competitor_leader(competitor=competitor).exists()

    def is_competitor_leader_in_current_season(self, competitor):
        # .first() as one competitor can be part of exactly one team in current season
        if not self.get_queryset().get_all_team_memberships_for_competitor(competitor=competitor):
            return False
        return self.get_queryset().get_team_memberships_for_active_season(competitor=competitor).first().is_leader
