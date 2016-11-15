from test_plus.test import TestCase

from loki.hack_fmi.models import Team, TeamMembership
from loki.seed.factories import (TeamFactory, SeasonFactory,
                                 RoomFactory, TeamMembershipFactory,
                                 CompetitorFactory)

from faker import Factory

faker = Factory.create()


class TestTeamManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

    def test_get_all_teams_for_competitor(self):
        self.assertEqual(1, Team.objects.count())
        self.assertEqual(1, Team.objects.get_all_teams_for_competitor(competitor=self.competitor).count())
        new_active_season = SeasonFactory(is_active=True)
        room = RoomFactory(season=new_active_season)
        team = TeamFactory(season=new_active_season, room=room)
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual(2, Team.objects.get_all_teams_for_competitor(competitor=self.competitor).count())

    def test_get_all_teams_for_current_season(self):
        self.assertEqual(1, Team.objects.count())
        self.assertEqual(1, Team.objects.get_all_teams_for_current_season(season=self.active_season).count())

        room = RoomFactory(season=self.active_season)
        team = TeamFactory(season=self.active_season, room=room)
        competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual(2, Team.objects.get_all_teams_for_current_season(season=self.active_season).count())

    def test_get_all_teams_for_competitor_for_current_season(self):
        self.assertEqual(self.team, Team.objects.get_all_teams_for_current_season(season=self.active_season).\
                                         get_all_teams_for_competitor(competitor=self.competitor).first())


class TestTeamMembershipManager(TestCase):
    def setUp(self):
        self.active_season = SeasonFactory(is_active=True)
        self.room = RoomFactory(season=self.active_season)
        self.team = TeamFactory(season=self.active_season, room=self.room)
        self.competitor = CompetitorFactory(email=faker.email())
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

    def test_list_all_teams_for_competitor(self):
        self.assertEqual(1, TeamMembership.objects.count())
        self.assertEqual([self.team], TeamMembership.objects.list_all_teams_for_competitor(competitor=self.competitor))
        new_active_season = SeasonFactory(is_active=True)
        room = RoomFactory(season=new_active_season)
        team = TeamFactory(season=new_active_season, room=room)
        self.team_membership = TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertEqual([self.team, team],
                         TeamMembership.objects.list_all_teams_for_competitor(competitor=self.competitor))

    def test_get_leader_of_team(self):
        self.assertEqual(self.competitor, TeamMembership.objects.get_leader_of_team(team=self.team))
