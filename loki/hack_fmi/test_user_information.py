from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Skill, Competitor, Season, Team, TeamMembership


class LoginTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.competitor.set_password('123')
        self.competitor.is_active = True
        self.competitor.save()
        self.season_active = Season.objects.create(
            name="season",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",

        )
        self.season_not_active = Season.objects.create(
            name="season",
            topic='TestTopic_2',
            is_active=False,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
        self.team = Team.objects.create(
            name='Pandas',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season_active,
        )
        self.team_dummy = Team.objects.create(
            name='Dummy',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season_not_active,
        )
        self.team_membership = TeamMembership.objects.create(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.team_membership = TeamMembership.objects.create(
            competitor=self.competitor,
            team=self.team_dummy,
            is_leader=True,
        )

    def test_get_data_after_login(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.competitor.email)
