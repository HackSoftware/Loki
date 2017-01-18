import json

from django.core.management import call_command
from django.conf import settings

from test_plus.test import TestCase

from ..models import Season, Team, Mentor, TeamMentorship


class PlacerTests(TestCase):
    def setUp(self):
        self.season = Season.objects.create(
            name="Season 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2015-5-1",
            mentor_pick_start_date="2015-4-1",
            mentor_pick_end_date="2015-5-1",
            make_team_dead_line="2016-5-1",
        )
        for i in range(1, 5):
            Team.objects.create(
                name='T{0}'.format(i),
                idea_description='GameDevelopers',
                repository='https://github.com/HackSoftware',
                season=self.season,
            )
        for i in range(1, 6):
            Mentor.objects.create(
                name='M{0}'.format(i),
                description='fancy mentor',
            )
        M1 = Mentor.objects.filter(name='M1').first()
        M2 = Mentor.objects.filter(name='M2').first()
        M3 = Mentor.objects.filter(name='M3').first()
        M4 = Mentor.objects.filter(name='M4').first()

        T1 = Team.objects.get(name='T1')
        T2 = Team.objects.get(name='T2')
        T3 = Team.objects.get(name='T3')

        TeamMentorship.objects.create(mentor=M1,
                                      team=T1)
        TeamMentorship.objects.create(mentor=M2,
                                      team=T1)
        TeamMentorship.objects.create(mentor=M3,
                                      team=T1)

        TeamMentorship.objects.create(mentor=M1,
                                      team=T2)
        TeamMentorship.objects.create(mentor=M2,
                                      team=T2)
        TeamMentorship.objects.create(mentor=M3,
                                      team=T2)
        TeamMentorship.objects.create(mentor=M4,
                                      team=T2)

        TeamMentorship.objects.create(mentor=M2,
                                      team=T3)
        TeamMentorship.objects.create(mentor=M3,
                                      team=T3)
        TeamMentorship.objects.create(mentor=M4,
                                      team=T3)

    def test_placer_command(self):
        call_command('placer')
        with open(settings.MEDIA_ROOT + '/placing.json') as f:
            data = json.load(f)

            self.assertEqual([], data['leftovers'])

            for tm in TeamMentorship.objects.all():
                self.assertIn(tm.mentor.name, data['placed'])
                self.assertIn(tm.team.name, data['placed'][tm.mentor.name].values())
