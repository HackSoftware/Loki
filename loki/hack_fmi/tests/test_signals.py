from test_plus.test import TestCase

from loki.seed.factories import (SeasonFactory,
                                 TeamFactory,
                                 CompetitorFactory, TeamMembershipFactory,
                                 SeasonCompetitorInfoFactory)

from ..models import SeasonCompetitorInfo

from faker import Factory

faker = Factory.create()


class TestTeamMembershipSignal(TestCase):
    def setUp(self):
        self.season = SeasonFactory()
        self.competitor = CompetitorFactory()
        self.season_competitor_info = SeasonCompetitorInfoFactory(competitor=self.competitor,
                                                                  season=self.season,
                                                                  looking_for_team=True)

    def test_signal_sets_to_false_looking_for_team_property_after_team_membership_is_created(self):
        team = TeamFactory(season=self.season)
        TeamMembershipFactory(team=team,
                              competitor=self.competitor,
                              is_leader=False)
        self.season_competitor_info.refresh_from_db()
        self.assertFalse(self.season_competitor_info.looking_for_team)


class TestSeasonCompetitorInfosSignal(TestCase):
    def test_season_competitor_info_is_created_when_new_active_season_is_added(self):
        competitor = CompetitorFactory()
        season = SeasonFactory(is_active=True)

        season_competitor_infos_count = SeasonCompetitorInfo.objects.filter(competitor=competitor,
                                                                            season=season).count()
        self.assertEqual(1, season_competitor_infos_count)
