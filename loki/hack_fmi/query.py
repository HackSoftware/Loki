from django.db import models


class TeamMembershipQuerySet(models.QuerySet):
    def get_all_team_memberships_for_competitor(self, competitor):
        return self.filter(competitor=competitor)

    def get_all_team_memberships_for_team(self, team):
        return self.filter(team=team)

    def get_team_membership_of_leader(self, team):
        return self.filter(team=team, is_leader=True)

    def get_team_memberships_for_active_season(self, competitor):
        return self.get_all_team_memberships_for_competitor(competitor=competitor).filter(team__season__is_active=True)

    def get_team_membership_for_competitor_leader(self, competitor):
        return self.get_all_team_memberships_for_competitor(competitor=competitor).filter(is_leader=True)


class TeamQuerySet(models.QuerySet):
    def get_all_teams_for_competitor(self, competitor):
        return self.filter(members__in=[competitor])

    def get_all_teams_for_current_season(self, season):
        return self.filter(season=season)

    def get_team_by_id(self, id):
        return self.filter(id=id)

    def get_team_by_name(self, name):
        return self.filter(name=name)


class TeamMentorshipQuerySet(models.QuerySet):
    def get_all_team_mentorships_for_team(self, team):
        return self.filter(team=team)


class CompetitorQuerySet(models.QuerySet):
    def get_competitor_by_email(self, email):
        return self.filter(email=email)


class InvitationQuerySet(models.QuerySet):
    def get_competitor_invitations_for_active_season(self, competitor):
        return self.filter(competitor=competitor).filter(team__season__is_active=True)
