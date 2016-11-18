import unittest
import collections
from django.core import mail
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.management.base import CommandError

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils
from test_plus.test import TestCase

from ..helper import date_increase, date_decrease
from ..models import (TeamMembership, Competitor,
                      Season, Team, Invitation, Room,
                      TeamMentorship, Mentor)

from loki.seed import factories

from faker import Factory

faker = Factory.create()


class TestSkillListAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = self.reverse('hack_fmi:skills')
        self.skill = factories.SkillFactory()

    def test_get_all_skills(self):
        skill2 = factories.SkillFactory()
        response = self.client.get(self.url)
        self.response_200(response)
        self.assertContains(response, self.skill.name)
        self.assertContains(response, skill2.name)


class TestMentorListAPIView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.company = factories.HackFmiPartnerFactory()
        self.active_season = factories.SeasonFactory(is_active=True)
        self.non_active_season = factories.SeasonFactory(is_active=False)
        self.url = reverse('hack_fmi:mentors')

    def test_get_all_mentors_for_current_active_season(self):

        self.assertEqual(Mentor.objects.all().count(), 0)

        mentor = factories.MentorFactory(from_company=self.company)
        mentor2 = factories.MentorFactory(from_company=self.company)
        self.active_season.mentor_set.add(mentor)
        self.active_season.mentor_set.add(mentor2)
        self.active_season.save()

        mentor3 = factories.MentorFactory(from_company=self.company)
        self.non_active_season.mentor_set.add(mentor3)
        self.non_active_season.save()

        response = self.client.get(self.url)
        mentors_for_current_season = self.active_season.mentor_set.count()

        self.response_200(response)
        self.assertEqual(len(response.data), mentors_for_current_season)
        self.assertContains(response, mentor.name)
        self.assertContains(response, mentor2.name)
        self.assertNotContains(response, mentor3.name)


class TestSeasonView(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(from_company=self.company)
        self.active_season = factories.SeasonFactory(is_active=True)
        self.non_active_season = factories.SeasonFactory(is_active=False)

    def test_get_active_season(self):
        url = self.reverse('hack_fmi:season')
        response = self.client.get(url)
        self.response_200(response)
        self.assertContains(response, self.active_season.name)
        self.assertNotContains(response, self.non_active_season.name)
        self.assertTrue(Season.objects.filter(is_active=True).exists())

    def test_season_deactivates_automatically(self):
        new_active_season = factories.SeasonFactory(is_active=True)
        self.assertTrue(Season.objects.filter(is_active=True).exists())
        self.assertFalse(Season.objects.get(name=self.active_season.name).is_active)
        self.assertTrue(Season.objects.get(name=new_active_season.name).is_active)


class TestPublicTeamView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(
            is_active=True
        )
        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season,
                                          room=self.room)
        self.url = reverse('hack_fmi:public_teams')

    def test_get_teams_for_current_season(self):
        teams_in_active_season = Team.objects.filter(season__is_active=True).count()

        response = self.client.get(self.url)

        self.response_200(response)
        self.assertEqual(len(response.data), teams_in_active_season)
        self.assertEqual(response.data[0]['name'], self.team.name)

    def test_get_teams_only_from_current_active_season(self):
        non_active_season = factories.SeasonFactory(
            is_active=False
        )
        room_for_non_active_season = factories.RoomFactory(season=non_active_season)
        team_in_non_active_season = factories.TeamFactory(
            name=faker.name(),
            season=non_active_season,
            room=room_for_non_active_season,
        )

        teams_in_active_season = Team.objects.filter(season__is_active=True).count()

        response = self.client.get(self.url)

        self.response_200(response)
        self.assertEqual(len(response.data), teams_in_active_season)
        self.assertEqual(response.data[0]['name'], self.team.name)
        self.assertNotEqual(response.data[0]['name'], team_in_non_active_season.name)

    def test_only_get_request_is_allowed_to_that_view(self):
        response = self.client.post(self.url)
        self.response_405(response)

        response = self.client.patch(self.url)
        self.response_405(response)

        response = self.client.delete(self.url)
        self.response_405(response)


class TestCreateJWTToken(TestCase):
    def test_create_jwt_token(self):
        competitor = factories.CompetitorFactory(email=faker.email())
        competitor.is_active = True
        competitor.set_password(factories.BaseUserFactory.password)
        competitor.save()

        data = {'email': competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        decoded_payload = utils.jwt_decode_handler(response.data['token'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload['email'], data['email'])


class TestMeAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(is_active=True)
        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season, room=self.room)
        self.competitor = factories.CompetitorFactory(email=faker.email())
        self.competitor.is_active = True
        self.competitor.set_password(factories.BaseUserFactory.password)
        self.competitor.save()
        self.team_membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                               team=self.team,
                                                               is_leader=True)

        data = {'email': self.competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

    def test_get_me(self):
        response = self.get('hack_fmi:me')
        self.response_200(response)
        """
        Assert if there are all the keys I need in the response.
        """
        key_equals = [True for k in ['teams', 'competitor_info', 'is_competitor'] if k in response.data.keys()]
        self.assertTrue(all(key_equals))

        competitor_info = {"email": self.competitor.email,
                           "first_name": self.competitor.first_name,
                           "last_name": self.competitor.last_name,
                           "is_vegetarian": self.competitor.is_vegetarian,
                           "known_skills": [],
                           "faculty_number": self.competitor.faculty_number,
                           "shirt_size": self.competitor.shirt_size,
                           "current_teammembership_set": [collections.OrderedDict((
                                ("competitor", self.competitor.id),
                                ("team", self.team.id),
                                ("is_leader", self.team_membership.is_leader)))],
                           "teammembership_set": [collections.OrderedDict((
                                ("competitor", self.competitor.id),
                                ("team", self.team.id),
                                ("is_leader", self.team_membership.is_leader)))],
                           "needs_work": self.competitor.needs_work,
                           "social_links": self.competitor.social_links}

        """
        In order to test if the competitor_info in the response.data is the proper one
        I make list of its values and join them (cannot use .values() method because the dict in the response
        is OrderedDict). After that I check if all the values in the data are the ones I want and assert it.
        """
        response_values = ", ".join([str(v) for v in response.data['competitor_info'].values()])
        data_equals = [True for val in competitor_info.values() if str(val) in response_values]
        self.assertTrue(all(data_equals))

        """
        Assert 'is_competitor' is the proper boolean.
        """
        self.assertEqual(response.data['is_competitor'], bool(self.competitor.get_competitor()))

        teams_info = [{"id": self.team.id,
                       "name": self.team.name,
                       "members": [{"email": self.competitor.email,
                                    "first_name": self.competitor.first_name,
                                    "last_name": self.competitor.last_name,
                                    "is_vegetarian": self.competitor.is_vegetarian,
                                    "known_skills": [],
                                    "faculty_number": self.competitor.faculty_number,
                                    "shirt_size": self.competitor.shirt_size,
                                    "current_teammembership_set": [collections.OrderedDict((
                                        ("competitor", self.competitor.id),
                                        ("team", self.team.id),
                                        ("is_leader", self.team_membership.is_leader)))],
                                    "teammembership_set": [collections.OrderedDict((
                                        ("competitor", self.competitor.id),
                                        ("team", self.team.id),
                                        ("is_leader", self.team_membership.is_leader)))],
                                    "needs_work": self.competitor.needs_work,
                                    "social_links": self.competitor.social_links}],
                       "season": self.active_season.id,
                       "leader_id": self.competitor.id}]
        """
        In order to test if the teams_info in the response.data is the proper one
        I make list of its values and join them (cannot use .values() method because 'teams' in response is
        list of OrderedDicts). After that I check if all the values in the data are the ones I want and assert it.
        """
        response_values = ", ".join([str(v) for v in response.data['teams']])
        data_equals = [True for val in teams_info if str(val) in response_values]
        self.assertTrue(all(data_equals))

    def test_post_me(self):
        response = self.post('hack_fmi:me')
        self.response_405(response)

    def test_get_with_wrong_jwt(self):
        self.token = faker.text()
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        response = self.get('hack_fmi:me')
        self.response_401(response)


class TestMeSeasonAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(is_active=True)
        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season, room=self.room)
        self.competitor = factories.CompetitorFactory(email=faker.email())
        self.competitor.is_active = True
        self.competitor.set_password(factories.BaseUserFactory.password)
        self.competitor.save()
        self.team_membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                               team=self.team,
                                                               is_leader=True)

        data = {'email': self.competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

    def test_get_me(self):
        response = self.get('hack_fmi:me-season', season_pk=self.active_season.id)
        self.response_200(response)
        """
        Assert if there are all the keys I need in the response.
        """
        key_equals = [True for k in ['is_competitor', 'competitor_info', 'team'] if k in response.data.keys()]
        self.assertTrue(all(key_equals))

    def test_post_me(self):
        response = self.post('hack_fmi:me-season')
        self.response_404(response)

    def test_get_with_wrong_jwt(self):
        self.token = faker.text()
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        response = self.get('hack_fmi:me-season', season_pk=self.active_season.id)
        self.response_401(response)

    def test_get_with_wrong_season_id(self):
        wrong_id = Season.objects.all().last().id + 1
        response = self.get('hack_fmi:me-season', season_pk=wrong_id)
        self.response_404(response)


class TestTeamAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(is_active=True)
        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season, room=self.room)
        self.competitor = factories.CompetitorFactory(email=faker.email())
        self.competitor.is_active = True
        self.competitor.set_password(factories.BaseUserFactory.password)
        self.competitor.save()
        self.team_membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                               team=self.team,
                                                               is_leader=False)

        data = {'email': self.competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

    def test_can_not_access_other_team_detail(self):
        self.client.credentials()
        response = self.get('hack_fmi:team-detail', pk=self.team.id)
        self.response_401(response)

    def test_competitor_can_get_team_information_for_his_team_in_active_season_within_the_season_deadlines(self):
        url = self.reverse('hack_fmi:team-list')

        response = self.client.get(url)
        self.response_200(response)

    def test_non_teamleaders_cant_change_team(self):
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph()
        }

        url = self.reverse('hack_fmi:team-detail', pk=self.team.id)
        response = self.client.patch(url, data)
        self.response_403(response)

    def test_only_leader_can_change_team(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        url = self.reverse('hack_fmi:team-detail', pk=self.team.id)

        response = self.client.patch(url, data)
        self.response_200(response)

        self.assertIsNotNone(Team.objects.get(name=data['name']))
        self.assertIsNotNone(Team.objects.get(idea_description=data['idea_description']))

    def test_user_can_get_to_teams_in_non_active_seasons(self):
        self.active_season.is_active = False
        self.active_season.save()

        url = self.reverse('hack_fmi:team-list')
        response = self.client.get(url)
        self.response_200(response)

    def test_user_cannot_change_teams_in_non_active_seasons(self):
        self.active_season.is_active = False
        self.active_season.save()
        self.team_membership.is_leader = True
        self.team_membership.save()

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        url = self.reverse('hack_fmi:team-detail', pk=self.team.id)
        response = self.client.patch(url, data)
        self.response_403(response)

    def test_leader_cannot_change_teams_in_non_active_seasons(self):
        self.active_season.is_active = False
        self.active_season.save()

        self.team_membership.is_leader = True
        self.team_membership.save()

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        url = self.reverse('hack_fmi:team-detail', pk=self.team.id)
        response = self.client.patch(url, data)
        self.response_403(response)

    def test_get_team_within_current_season_deadlines(self):
        url = self.reverse("hack_fmi:team-detail", pk=self.team.id)
        response = self.client.get(url)
        self.response_200(response)

    def test_cannot_change_team_out_of_the_current_season_deadline(self):
        self.active_season.make_team_dead_line = date_increase(10)
        self.active_season.save()

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        url = self.reverse("hack_fmi:team-detail", pk=self.team.id)
        response = self.client.patch(url, data)
        self.response_403(response)

    def test_whether_when_you_register_your_own_team_you_become_leader_of_that_team(self):
        skill = factories.SkillFactory()
        team_data = {
            'name': faker.name(),
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],
        }

        self.assertFalse(Team.objects.filter(name=team_data['name']).exists())

        url = self.reverse("hack_fmi:team-list")
        response = self.client.post(url, team_data)
        self.response_201(response)
        self.assertTrue(Team.objects.filter(name=team_data['name']).exists())
        self.assertEqual(len(response.data['members']), 1)
        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor, is_leader=True).exists())

    def test_cant_register_team_that_has_the_same_name(self):
        skill = factories.SkillFactory()

        self.assertTrue(Team.objects.filter(name=self.team.name).exists())
        self.assertEquals(Team.objects.filter(name=self.team.name).count(), 1)

        team_data = {
            'name': self.team.name,
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],
        }

        url = self.reverse("hack_fmi:team-list")
        response = self.client.post(url, team_data)

        self.response_403(response)
        self.assertEquals(Team.objects.filter(name=self.team.name).count(), 1)

    def test_cant_register_other_team_if_you_are_a_leader_of_already_existing_team(self):
        self.team_membership.is_leader = True
        self.team_membership.save()

        skill = factories.SkillFactory()
        team_data = {
            'name': faker.name(),
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],
        }

        url = self.reverse("hack_fmi:team-list")
        response = self.client.post(url, team_data)
        self.response_403(response)

class OnBoardCompetitorAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_user = factories.BaseUserFactory(email=faker.email())
        self.base_user.is_active = True
        self.base_user.save()
        self.skill = factories.SkillFactory()

        data = {'email': self.base_user.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']

    def test_onboarding_base_user_with_correct_authorization_token_and_correct_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        data = {
            "known_skills": [self.skill.id],
            "shirt_size": 2,
            "needs_work": False,
            "is_vegetarian": False,
            "social_links": faker.text()
        }

        response = self.client.post(self.reverse('hack_fmi:onboard_competitor'), data=data)
        self.response_201(response)

        self.assertEquals(1, Competitor.objects.all().count())

    def test_onboarding_base_user_with_uncorrect_authorization_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + faker.text())
        data = {
            "known_skills": [self.skill.id],
            "shirt_size": 2,
            "needs_work": False,
            "is_vegetarian": False,
            "social_links": faker.text()
        }

        response = self.client.post(self.reverse('hack_fmi:onboard_competitor'), data=data)
        self.response_401(response)

        self.assertEquals(0, Competitor.objects.all().count())

    def test_onboarding_baseuser_with_correct_token_and_uncorrect_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        data = {
            "baba": faker.text()
        }

        response = self.client.post(self.reverse('hack_fmi:onboard_competitor'), data=data)
        self.assertEquals(400, response.status_code)

        self.assertEquals(0, Competitor.objects.all().count())

class TestTeamMembershipAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(from_company=self.company)

        self.active_season = factories.SeasonFactory(is_active=True)
        self.non_active_season = factories.SeasonFactory(is_active=False)

        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season)
        self.non_active_team = factories.TeamFactory(season=self.non_active_season)

        self.competitor = factories.CompetitorFactory(email=faker.email())
        self.competitor.is_active = True
        self.competitor.set_password(factories.BaseUserFactory.password)
        self.competitor.save()
        data = {'email': self.competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']

    def test_user_cant_leave_team_if_he_has_not_been_a_member_in_that_team(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        other_competitor = factories.CompetitorFactory(email=faker.email())
        other_membership = factories.TeamMembershipFactory(competitor=other_competitor,
                                                           team=self.team,
                                                           is_leader=False)
        factories.TeamMembershipFactory(competitor=self.competitor,
                                        team=self.team,
                                        is_leader=True)

        url = self.reverse('hack_fmi:team_membership', pk=other_membership.id)

        response = self.client.delete(url)

        self.response_403(response)

    def test_cant_leave_team_if_you_are_not_logged_as_hackfmi_user(self):
        # In case you are logged in as a Student, but you are not Competitor
        other_competitor = factories.StudentFactory(email=faker.email())
        other_competitor.is_active = True
        other_competitor.set_password(factories.BaseUserFactory.password)
        other_competitor.save()
        self.assertFalse(Competitor.objects.filter(email=other_competitor.email).exists())

        data = {'email': other_competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)

        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

        url = self.reverse('hack_fmi:team_membership', pk=membership.id)

        response = self.client.delete(url)

        self.response_403(response)

    def test_cant_leave_team_if_you_are_not_logged_in(self):

        other_competitor = factories.StudentFactory(email=faker.email())
        self.assertFalse(Competitor.objects.filter(email=other_competitor.email).exists())

        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=True)

        url = self.reverse('hack_fmi:team_membership', pk=membership.id)

        response = self.client.delete(url)

        self.response_401(response)

    def test_leave_team_from_non_active_season(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.non_active_team,
                                                     is_leader=True)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_non_team_leader_leaves_team(self):
        # You can leave team without being a team leader
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=self.team,
                                                     is_leader=False)

        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())

    def test_delete_team_if_competitor_is_leader(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        team = factories.TeamFactory(name=faker.name(),
                                     season=self.active_season)
        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=True)

        self.assertEqual(team.get_leader(), self.competitor)
        self.assertTrue(Team.objects.filter(name=team.name).exists())
        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(name=team.name).exists())
        self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())

    def test_cant_delete_team_when_leaving_if_you_are_not_leader(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        team = factories.TeamFactory(name=faker.name(),
                                     season=self.active_season)
        membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                     team=team,
                                                     is_leader=False)

        self.assertNotEqual(team.get_leader(), self.competitor)
        self.assertTrue(Team.objects.filter(name=team.name).exists())
        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Team.objects.filter(name=team.name).exists())
        self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())


class TestInvitationViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.season = factories.SeasonFactory(
            is_active=True,
        )
        self.recipient = factories.CompetitorFactory(email=faker.email())
        self.recipient.is_active = True
        self.recipient.set_password(factories.BaseUserFactory.password)
        self.recipient.save()
        data = {'email': self.recipient.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        self.team = factories.TeamFactory(name=faker.name(),
                                          season=self.season)
        self.token = response.data['token']

    def test_cant_send_invitation_for_joining_team_if_request_user_not_a_competitor(self):
        non_competitor = factories.BaseUserFactory(email=faker.email())
        non_competitor.is_active = True
        non_competitor.set_password(factories.BaseUserFactory.password)
        non_competitor.save()
        data = {'email': non_competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': non_competitor.email}
        response = self.client.post(url, data)
        self.response_403(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_invitation_for_team_to_other_competitor(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        """
        Every time a test is run, SeasonFactory generates random max_team_members_count.
        That's why we intentionaly specify max_team_members_count.
        """
        self.season.max_team_members_count = 2
        self.season.save()

        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team,
                                        is_leader=True)

        receiver = factories.CompetitorFactory(email=faker.email())

        self.assertEquals(Invitation.objects.count(), 0)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': receiver.email}
        response = self.client.post(url, data)
        self.response_201(response)
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.first().team.id, self.team.id)
        self.assertEqual(Invitation.objects.first().competitor.id, receiver.id)
        self.assertEqual(len(mail.outbox), 1)

    def test_sent_email_after_an_invitation_is_made(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team,
                                        is_leader=True)

        receiver = factories.CompetitorFactory(email=faker.email())

        self.assertEquals(Invitation.objects.count(), 0)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': receiver.email}
        response = self.client.post(url, data)
        self.response_201(response)
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.first().team.id, self.team.id)
        self.assertEqual(Invitation.objects.first().competitor.id, receiver.id)
        self.assertEqual(len(mail.outbox), 1)

    def test_non_leaders_cant_send_invitations(self):
        non_leader = factories.CompetitorFactory(email=faker.email())
        non_leader.is_active = True
        non_leader.set_password(factories.BaseUserFactory.password)
        non_leader.save()
        data = {'email': non_leader.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)

        factories.TeamMembershipFactory(competitor=non_leader,
                                        team=self.team,
                                        is_leader=False)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': faker.word() + faker.email()}
        response = self.client.post(url, data,)

        self.response_403(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_invitation_to_not_existing_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        """
        Every time a test is run, SeasonFactory generates random max_team_members_count.
        That's why we intentionaly specifi max_team_members_count.
        """
        self.season.max_team_members_count = 2
        self.season.save()

        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team,
                                        is_leader=True)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': faker.word() + faker.email()}
        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_invitation_twice_to_same_competitor(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team,
                                        is_leader=True)
        Invitation.objects.create(team=self.team,
                                  competitor=self.recipient)
        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': self.recipient.email}
        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_invitation_when_team_is_full(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        self.season.max_team_members_count = 2
        self.season.save()

        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team,
                                        is_leader=True)

        competitor2 = factories.CompetitorFactory(email=faker.email())

        factories.TeamMembershipFactory(competitor=competitor2,
                                        team=self.team,
                                        is_leader=False)

        self.assertEqual(TeamMembership.objects.filter(team=self.team).count(), 2)

        url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': self.recipient.email}

        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(TeamMembership.objects.filter(team=self.team).count(), 2)
        self.assertEqual(len(mail.outbox), 0)

    def test_cant_send_invitation_to_user_that_already_has_team(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        TeamMembership(team=self.team,
                       competitor=self.recipient,
                       is_leader=True)

        self.receiver = factories.CompetitorFactory(email=faker.email())
        factories.InvitationFactory(team=self.team,
                                    competitor=self.recipient)

        receiver_team = factories.TeamFactory(name=faker.name(),
                                              season=self.season)

        factories.TeamMembershipFactory(team=receiver_team,
                                        competitor=self.receiver)

        url = self.reverse('hack_fmi:invitation-list')
        data = {
            'competitor_email': self.receiver.email
        }
        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(len(mail.outbox), 0)

    def test_user_cant_get_his_invitations_if_not_being_hackfmi_user(self):
        self.client.credentials()

        url = self.reverse('hack_fmi:invitation-list')
        response = self.client.get(url)

        self.response_401(response)

    def test_user_can_get_his_invitations_if_hackfmi_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        factories.InvitationFactory(team=self.team,
                                    competitor=self.recipient)

        url = self.reverse('hack_fmi:invitation-list')
        response = self.client.get(url)

        self.response_200(response)
        self.assertEqual(len(response.data), 1)

    def test_cant_accept_invitation_if_not_authenticated(self):
        self.client.credentials()
        inv = factories.InvitationFactory()

        url = self.reverse('hack_fmi:invitation-accept', pk=inv.id)

        response = self.client.post(url)

        self.response_401(response)

    def test_cant_accept_invitation_if_not_hackfmi_user(self):
        user = factories.BaseUserFactory(email=faker.email())
        user.is_active = True
        user.set_password(factories.BaseUserFactory.password)
        user.save()
        data = {'email': user.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)
        inv = factories.InvitationFactory()

        url = self.reverse('hack_fmi:invitation-accept', pk=inv.id)

        response = self.client.post(url)

        self.response_403(response)

    def test_accept_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        inv = factories.InvitationFactory(team=self.team,
                                          competitor=self.recipient)
        self.assertEqual(Invitation.objects.all().count(), 1)
        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)
        self.response_200(response)
        self.assertEqual(Invitation.objects.all().count(), 0)
        self.\
            assertTrue(TeamMembership.objects.filter(team=inv.team, competitor=inv.competitor).exists())

    def test_cant_accept_non_existing_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        non_existing_invitation_id = faker.random_number(digits=1)
        self.assertFalse(Invitation.objects.filter(id=non_existing_invitation_id).exists())
        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': non_existing_invitation_id})
        response = self.client.post(url)
        self.response_404(response)

    def test_accept_invitation_already_has_team(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        factories.TeamMembershipFactory(competitor=self.recipient,
                                        team=self.team)

        inv = factories.InvitationFactory(team=self.team,
                                          competitor=self.recipient)

        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 1)

        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)

        self.response_403(response)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 1)

    def test_cannot_accept_invitation_that_is_not_dedicated_to_request_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        another_competitor = factories.CompetitorFactory()
        inv = factories.InvitationFactory(team=self.team,
                                          competitor=another_competitor)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 0)

        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})
        response = self.client.post(url)
        self.response_403(response)

        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 0)

    def test_can_accept_invitation_if_you_are_a_leader_in_non_active_season(self):
        pass

    def test_can_not_accept_invitation_to_other_team_if_you_are_a_leader_in_current_season(self):
        receiver = factories.CompetitorFactory(email=faker.email())
        receiver.is_active = True
        receiver.set_password(factories.BaseUserFactory.password)
        receiver.save()
        data = {'email': receiver.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        receiver_token = response.data['token']

        sender = factories.CompetitorFactory(email=faker.email())
        sender.is_active = True
        sender.set_password(factories.BaseUserFactory.password)
        sender.save()
        data = {'email': sender.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        sender_token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + sender_token)

        factories.TeamMembershipFactory(competitor=sender,
                                        team=self.team,
                                        is_leader=True)

        send_url = self.reverse('hack_fmi:invitation-list')
        data = {
            'competitor_email': receiver.email
        }
        response = self.client.post(send_url, data)

        self.response_201(response)
        self.assertTrue(Invitation.objects.filter(competitor=receiver,
                                                  team=self.team).exists())
        inv = Invitation.objects.get(competitor=receiver,
                                     team=self.team)

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + receiver_token)

        another_team = factories.TeamFactory(season=self.season)
        factories.TeamMembershipFactory(competitor=receiver,
                                        team=another_team,
                                        is_leader=True)

        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 2)

        url = self.reverse('hack_fmi:invitation-accept', pk=inv.id)

        response = self.client.post(url)
        self.response_403(response)

        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 2)

    def test_user_cant_delete_invitation_if_not_hackfmi_user(self):
        user = factories.BaseUserFactory(email=faker.email())
        user.is_active = True
        user.set_password(factories.BaseUserFactory.password)
        user.save()
        data = {'email': user.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)
        inv = factories.InvitationFactory()

        url = self.reverse('hack_fmi:invitation-detail', pk=inv.id)

        response = self.client.delete(url)

        self.response_403(response)

    def test_cant_delete_wrongly_dedicated_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        another_competitor = factories.CompetitorFactory()
        inv = factories.InvitationFactory(team=self.team,
                                          competitor=another_competitor)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 0)

        url = self.reverse('hack_fmi:invitation-detail', pk=inv.id)
        response = self.client.delete(url)
        self.response_403(response)

        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 0)

    def test_delete_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        inv = factories.InvitationFactory(team=self.team,
                                          competitor=self.recipient)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(TeamMembership.objects.count(), 0)

        url = self.reverse('hack_fmi:invitation-detail', pk=inv.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        self.assertEqual(Invitation.objects.count(), 0)
        self.assertEqual(TeamMembership.objects.count(), 0)


class TestTeamMentorshipAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(is_active=True)
        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season, room=self.room)
        self.competitor = factories.CompetitorFactory(email=faker.email())
        self.competitor.is_active = True
        self.competitor.set_password(factories.BaseUserFactory.password)
        self.competitor.save()
        self.team_membership = factories.TeamMembershipFactory(competitor=self.competitor,
                                                               team=self.team,
                                                               is_leader=True)

        data = {'email': self.competitor.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)

        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(from_company=self.company)

    def test_cannot_assign_mentor_if_you_are_not_hackfmi_user(self):
        self.client.credentials()
        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)

        self.response_401(response)

    def test_cannot_assign_mentor_if_not_leader_of_team(self):
        self.team_membership.is_leader = False
        self.team_membership.save()

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)

        self.response_403(response)

    def test_can_assign_mentor_if_leader_of_team(self):
        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)

        self.response_201(response)
        self.assertTrue(TeamMentorship.objects.filter(team=data['team']).exists())
        self.assertTrue(TeamMentorship.objects.filter(mentor=data['mentor']).exists())

    def test_assign_more_than_allowed_mentors_for_that_season(self):
        self.active_season.max_mentor_pick = 1
        self.active_season.save()

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)
        self.response_201(response)

        new_mentor = factories.MentorFactory(from_company=self.company)
        new_data = {'team': self.team.id,
                    'mentor': new_mentor.id,
                    }

        response = self.client.post(url, new_data)
        self.response_403(response)

    def test_assign_mentor_before_mentor_pick_has_started(self):
        self.active_season.mentor_pick_start_date = date_increase(10)
        self.active_season.mentor_pick_end_date = date_increase(10)
        self.active_season.save()

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)
        self.response_403(response)

    def test_assign_mentor_after_mentor_pick_has_ended(self):
        self.active_season.mentor_pick_start_date = date_decrease(10)
        self.active_season.mentor_pick_end_date = date_decrease(10)
        self.active_season.save()

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)
        self.response_403(response)

    def test_cannot_remove_mentor_from_team_if_not_teamleader(self):
        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)
        self.response_201(response)
        self.assertEqual(TeamMentorship.objects.filter(team=data['team']).count(), 1)

        self.team_membership.is_leader = False
        self.team_membership.save()
        existing_mentorship = TeamMentorship.objects.get(team=data['team'])
        url = self.reverse('hack_fmi:team_mentorship', pk=existing_mentorship.id)
        response = self.client.delete(url)
        self.response_403(response)
        self.assertEqual(TeamMentorship.objects.filter(team=data['team']).count(), 1)

    def test_can_remove_mentor_from_team_if_teamleader(self):
        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        self.assertEqual(TeamMentorship.objects.filter(team=data['team']).count(), 0)
        url = reverse('hack_fmi:team_mentorship')
        response = self.client.post(url, data)
        self.response_201(response)
        self.assertEqual(TeamMentorship.objects.filter(team=data['team']).count(), 1)
        existing_mentorship = TeamMentorship.objects.get(team=data['team'])

        url = self.reverse('hack_fmi:team_mentorship', pk=existing_mentorship.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMentorship.objects.filter(team=data['team']).count(), 0)


@unittest.skip('Skip until further implementation of Hackathon system')
class TestRooms(TestCase):

    def setUp(self):
        self.season = Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline=date_increase(10),
            mentor_pick_start_date=date_increase(15),
            mentor_pick_end_date=date_increase(25),
            make_team_dead_line=date_increase(20),
        )
        for i in range(10):
            Team.objects.create(
                name='Pandas{0}'.format(i),
                idea_description='GameDevelopers',
                repository='https://github.com/HackSoftware',
                season=self.season,
            )
        for i in [1, 4, 10]:
            Room.objects.create(
                number=100 + i,
                season=self.season,
                capacity=i,
            )

    def test_fill_rooms(self):
        call_command('fillrooms')
        for team in Team.objects.all():
            self.assertTrue(team.room.number)

    def test_more_teams_than_rooms(self):
        for i in range(10):
            Team.objects.create(
                name='Pandas{0}'.format(i + 15),
                idea_description='GameDevelopers',
                repository='https://github.com/HackSoftware',
                season=self.season,
            )
        with self.assertRaises(CommandError):
            call_command('fillrooms')
