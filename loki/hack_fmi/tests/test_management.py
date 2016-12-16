from django.core.management import call_command

from test_plus.test import TestCase

from ..helper import get_date_with_timedelta
from ..models import BlackListToken
from loki.hack_fmi.models import Team
from loki.seed.factories import TeamFactory, SeasonFactory, RoomFactory
from faker import Factory

faker = Factory.create()


class TestJWTCleanCommand(TestCase):

    def test_clean_old_jwt_token_commands(self):
        """
        The command deletes all the BlackListTokens that are older than one week.
        get_date_with_timedelta(-7) gives us a date that is older with 7 days from now
        """

        older_than_week_date = get_date_with_timedelta(days=-7)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=older_than_week_date)
        self.assertTrue(BlackListToken.objects.exists())
        call_command('clean_old_jwt_tokens')
        self.assertFalse(BlackListToken.objects.exists())

    def test_tokens_that_are_not_expired_yet_are_not_deleted(self):
        """
        The command should not delete the BlackListTokens that are not expored yet.
        """

        older_than_week_date = get_date_with_timedelta(days=-7)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=older_than_week_date)
        within_week_date = get_date_with_timedelta(days=-2)
        BlackListToken.objects.create(token=faker.text(),
                                      created_at=within_week_date)
        self.assertEqual(BlackListToken.objects.count(), 2)
        call_command('clean_old_jwt_tokens')
        self.assertEqual(BlackListToken.objects.count(), 1)
        self.assertEqual(BlackListToken.objects.first().created_at, within_week_date)


class FillRoomsCommandTest(TestCase):

    def setUp(self):
        self.teams_count = 10
        self.active_season = SeasonFactory(is_active=True)
        self.room1 = RoomFactory(season=self.active_season, capacity=3)
        self.room2 = RoomFactory(season=self.active_season, capacity=4)
        self.room3 = RoomFactory(season=self.active_season, capacity=4)

    def test_fill_empty_rooms_if_all_rooms_were_empty(self):
        teams = [TeamFactory(season=self.active_season, room=None) for _ in range(self.teams_count)]
        self.assertEqual(0, Team.objects.filter(season=self.active_season, room__isnull=False).count())
        call_command('fillrooms')
        self.assertEqual(self.teams_count, Team.objects.filter(season=self.active_season,
                                                               room__isnull=False).count())

    def test_fill_teams_in_rooms_if_team_capacity_less_than_team_count(self):
        self.room2.capacity=2
        self.room2.save()
        self.room3.capacity=1
        self.room3.save()

        teams = [TeamFactory(season=self.active_season, room=None) for _ in range(self.teams_count)]
        self.assertEqual(0, Team.objects.filter(season=self.active_season, room__isnull=False).count())
        call_command('fillrooms')
        self.assertEqual(self.teams_count, Team.objects.filter(season=self.active_season,
                                                               room__isnull=False).count())
        self.assertFalse(Team.objects.filter(season=self.active_season,
                                             room__isnull=True).exists())


    def test_fill_empty_rooms_if_full_rooms_exist(self):
        TeamFactory(season=self.active_season, room=self.room1)
        TeamFactory(season=self.active_season, room=self.room1)
        TeamFactory(season=self.active_season, room=self.room2)
        TeamFactory(season=self.active_season, room=self.room2)

        self.assertEqual(4, Team.objects.filter(season=self.active_season,
                                                room__isnull=False).count())
        teams_and_rooms = Team.objects.filter(season=self.active_season, room__isnull=False).values('id', 'room')

        team = TeamFactory(season=self.active_season, room=None)
        call_command('fillrooms')
        updated_teams_rooms = Team.objects.filter(season=self.active_season, room__isnull=False).values('id', 'room')

        for tr in teams_and_rooms:
            self.assertIn(tr, updated_teams_rooms)

        team.refresh_from_db()
        team_info = {'id': team.id, 'room': team.room.id}
        self.assertIn(team_info, updated_teams_rooms)
        self.assertEqual(5, Team.objects.filter(room__isnull=False).count())
