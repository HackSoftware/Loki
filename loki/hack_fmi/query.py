from django.db import models


class TeamMembershipQuerySet(models.QuerySet):
    def get_all_team_memberships_for_competitor(self, competitor):
        return self.filter(competitor=competitor)

    def get_team_membership_of_leader(self, team):
        return self.filter(team=team, is_leader=True)

    def get_teams_for_active_season(self, competitor):
        return self.get_all_team_memberships_for_competitor(competitor=competitor).filter(team__season__is_active=True)


class TeamQuerySet(models.QuerySet):
    def get_all_teams_for_competitor(self, competitor):
        return self.filter(members__in=[competitor])

    def get_all_teams_for_current_season(self, season):
        return self.filter(season=season)
