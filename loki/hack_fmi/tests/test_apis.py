import unittest
import collections
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.management.base import CommandError

from django.core.mail import EmailMultiAlternatives

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt import utils
from test_plus.test import TestCase

from ..helper import date_increase, date_decrease
from ..models import (TeamMembership,
                      Season, Team, Invitation, Room,
                      TeamMentorship, Mentor)

from loki.seed import factories

from faker import Factory

faker = Factory.create()


class SkillListAPITests(TestCase):

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


class MentorListAPIViewTest(TestCase):

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


class SeasonViewTest(TestCase):

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


class PublicTeamViewTest(TestCase):

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


class CreateJWTToken(TestCase):
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
                           "current_teammembership_set": [collections.OrderedDict((("competitor", self.competitor.id),
                                                                                   ("team", self.team.id),
                                                                                   ("is_leader", self.team_membership.is_leader)))],
                           "teammembership_set": [collections.OrderedDict((("competitor", self.competitor.id),
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
                                    "current_teammembership_set": [collections.OrderedDict((("competitor", self.competitor.id),
                                                                                            ("team", self.team.id),
                                                                                            ("is_leader", self.team_membership.is_leader)))],
                                    "teammembership_set": [collections.OrderedDict((("competitor", self.competitor.id),
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


class TeamAPITest(TestCase):

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


class TeamMembershipAPITest(TestCase):

    def setUp(self):
        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(
            from_company=self.company)
        self.client = APIClient()

        self.active_season = factories.SeasonFactory(is_active=True)
        self.non_active_season = factories.SeasonFactory(is_active=False)

        self.room = factories.RoomFactory(season=self.active_season)
        self.team = factories.TeamFactory(season=self.active_season)
        self.non_active_team = factories.TeamFactory(season=self.non_active_season)

        self.competitor = factories.CompetitorFactory(email=faker.email())

    def test_user_cant_leave_team_if_he_has_not_been_a_member_in_that_team(self):
        other_competitor = factories.CompetitorFactory(email=faker.email())
        other_membership = factories.TeamMembershipFactory(competitor=other_competitor,
                                                           team=self.team,
                                                           is_leader=False)
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': other_membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_cant_leave_team_if_yoy_are_not_a_hackfmi_user(self):
        other_competitor = factories.StudentFactory(
            email=faker.email())
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )

        self.client.force_authenticate(other_competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_leave_team_from_non_active_season(self):
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.non_active_team,
            is_leader=True,
        )

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_non_team_leader_leaves_team(self):
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=False,
        )

        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())
        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())

    def test_delete_team_if_competitor_is_leader(self):
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.active_season,
        )
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=team,
            is_leader=True,
        )
        self.assertEqual(team.get_leader(), self.competitor)
        self.assertTrue(Team.objects.filter(name=team.name).exists())
        self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(name=team.name).exists())
        self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())


class InvitationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.season = factories.SeasonFactory(
            is_active=True,
        )

    def test_send_invitation_for_team(self):
        """
        Every time a test is run, SeasonFactory generates random max_team_members_count.
        That's why we intentionaly specifi max_team_members_count.
        """
        self.season.max_team_members_count = 2
        self.season.save()

        recipient = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=recipient,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(user=recipient)

        receiver = factories.CompetitorFactory(
            email=faker.email()
        )

        url = reverse('hack_fmi:invitation-list')
        data = {'competitor_email': receiver.email}
        response = self.client.post(url, data)

        self.response_201(response)
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.first().team.id, team.id)
        self.assertEqual(Invitation.objects.first().competitor.id, receiver.id)

    def test_if_email_is_sent_to_user(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        subject = "Invitation for hackFMI membership"
        body = faker.paragraph()

        msg = EmailMultiAlternatives(subject=subject,
                                     body=body,
                                     from_email=settings.DJANGO_DEFAULT_FROM_EMAIL,
                                     to=[competitor.email])

        response = msg.send()

        self.assertEqual(response, 1)

    def test_non_leaders_cant_send_invitations(self):
        competitor = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=False,
        )
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:invitation-list')
        data = {'competitor_email': faker.word() + faker.email()}
        response = self.client.post(url, data,)

        self.response_403(response)

    def test_send_invitation_to_not_existing_user(self):
        """
        Every time a test is run, SeasonFactory generates random max_team_members_count.
        That's why we intentionaly specifi max_team_members_count.
        """
        self.season.max_team_members_count = 2
        self.season.save()

        recipient = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=recipient,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(user=recipient)

        url = reverse('hack_fmi:invitation-list')
        data = {'competitor_email': faker.word() + faker.email()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_invitation_twice_to_same_competitor(self):
        recipient = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=recipient,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(user=recipient)

        Invitation.objects.create(
            team=team,
            competitor=recipient,
        )
        url = reverse('hack_fmi:invitation-list')
        data = {'competitor_email': recipient.email}
        response = self.client.post(url, data)

        self.response_403(response)

    def test_send_invitation_when_team_is_full(self):
        self.season.max_team_members_count = 2
        self.season.save()

        recipient = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=recipient,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(user=recipient)

        competitor2 = factories.CompetitorFactory(
            email=faker.email()
        )

        factories.TeamMembershipFactory(
            competitor=competitor2,
            team=team,
            is_leader=False,
        )

        self.assertEqual(TeamMembership.objects.filter(team=team).count(), 2)

        url = reverse('hack_fmi:invitation-list')
        data = {'competitor_email': recipient.email}

        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(TeamMembership.objects.filter(team=team).count(), 2)

    def test_user_cant_get_his_invitations_if_not_being_hackfmi_user(self):
        user = factories.BaseUserFactory(
            email=faker.email()
        )
        self.client.force_authenticate(user=user)

        url = reverse('hack_fmi:invitation-list')
        response = self.client.get(url)

        self.response_403(response)

    def test_user_can_get_his_invitations_if_hackfmi_user(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.InvitationFactory(
            team=team,
            competitor=competitor
        )
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:invitation-list')
        response = self.client.get(url)

        self.response_200(response)
        self.assertEqual(len(response.data), 1)

    def test_send_invitation_to_user_that_already_has_team(self):
        recipient = factories.CompetitorFactory(
            email=faker.email(),
        )
        receiver = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=recipient,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(user=recipient)

        receiver_team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )

        factories.TeamMembershipFactory(
            team=receiver_team,
            competitor=receiver,
        )

        url = reverse('hack_fmi:invitation-list')
        data = {
            'competitor_email': receiver.email
        }
        response = self.client.post(url, data)

        self.response_403(response)

    def test_accept_invitation(self):
        competitor_not_leader = factories.CompetitorFactory(
            email=faker.email(),
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        self.client.force_authenticate(user=competitor_not_leader)

        inv = factories.InvitationFactory(
            team=team,
            competitor=competitor_not_leader
        )
        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)
        self.response_200(response)
        self.assertEqual(Invitation.objects.all().count(), 0)
        self.\
            assertTrue(TeamMembership.objects.filter(team=inv.team, competitor=inv.competitor).exists())

    def test_accept_invitation_already_has_team(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.season
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
        )

        inv = factories.InvitationFactory(
            team=team,
            competitor=competitor
        )
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)

        self.response_403(response)

    def test_can_not_accept_invitation_to_other_team_if_you_are_a_leader(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.season
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(competitor)

        inv = factories.InvitationFactory(
            team=team,
            competitor=competitor
        )

# class TeamMembershipAPITest(TestCase):

#     def setUp(self):
#         self.company = factories.HackFmiPartnerFactory()
#         self.mentor = factories.MentorFactory(
#             from_company=self.company)
#         self.client = APIClient()

#         self.active_season = factories.SeasonFactory(
#             is_active=True
#         )
#         self.non_active_season = factories.SeasonFactory(
#             is_active=False)

#         self.room = factories.RoomFactory(
#             season=self.active_season)
#         self.team = factories.TeamFactory(
#             season=self.active_season,
#         )
#         self.non_active_team = factories.TeamFactory(
#             season=self.non_active_season)

#         self.competitor = factories.CompetitorFactory(
#             email=faker.email())

#     def test_user_cant_leave_team_if_he_has_not_been_a_member_in_that_team(self):
#         other_competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         other_membership = factories.TeamMembershipFactory(
#             competitor=other_competitor,
#             team=self.team,
#             is_leader=False,
#         )
#         factories.TeamMembershipFactory(
#             competitor=self.competitor,
#             team=self.team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(self.competitor)

#         url = reverse('hack_fmi:team_membership', kwargs={'pk': other_membership.id})

#         response = self.client.delete(url)

#         self.response_403(response)

#     def test_cant_leave_team_if_yoy_are_not_a_hackfmi_user(self):
#         other_competitor = factories.StudentFactory(
#             email=faker.email())
#         membership = factories.TeamMembershipFactory(
#             competitor=self.competitor,
#             team=self.team,
#             is_leader=True,
#         )

#         self.client.force_authenticate(other_competitor)

#         url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

#         response = self.client.delete(url)

#         self.response_403(response)

#     def test_leave_team_from_non_active_season(self):
#         membership = factories.TeamMembershipFactory(
#             competitor=self.competitor,
#             team=self.non_active_team,
#             is_leader=True,
#         )

#         self.client.force_authenticate(self.competitor)

#         url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

#         response = self.client.delete(url)

#         self.response_403(response)

#     def test_non_team_leader_leaves_team(self):
#         membership = factories.TeamMembershipFactory(
#             competitor=self.competitor,
#             team=self.team,
#             is_leader=False,
#         )

#         self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())
#         self.client.force_authenticate(self.competitor)

#         url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())

#     def test_delete_team_if_competitor_is_leader(self):
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.active_season,
#         )
#         membership = factories.TeamMembershipFactory(
#             competitor=self.competitor,
#             team=team,
#             is_leader=True,
#         )
#         self.assertEqual(team.get_leader(), self.competitor)
#         self.assertTrue(Team.objects.filter(name=team.name).exists())
#         self.assertTrue(TeamMembership.objects.filter(competitor=self.competitor).exists())

#         self.client.force_authenticate(self.competitor)

#         url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Team.objects.filter(name=team.name).exists())
#         self.assertFalse(TeamMembership.objects.filter(competitor=self.competitor).exists())


# class InvitationTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#         self.season = factories.SeasonFactory(
#             is_active=True,
#         )

#     def test_send_invitation_for_team(self):
#         """
#         Every time a test is run, SeasonFactory generates random max_team_members_count.
#         That's why we intentionaly specifi max_team_members_count.
#         """
#         self.season.max_team_members_count = 2
#         self.season.save()

#         recipient = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=recipient,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(user=recipient)

#         receiver = factories.CompetitorFactory(
#             email=faker.email()
#         )

#         url = reverse('hack_fmi:invitation-list')
#         data = {'competitor_email': receiver.email}
#         response = self.client.post(url, data)

#         self.response_201(response)
#         self.assertEquals(Invitation.objects.count(), 1)
#         self.assertEqual(Invitation.objects.first().team.id, team.id)
#         self.assertEqual(Invitation.objects.first().competitor.id, receiver.id)

#     def test_if_email_is_sent_to_user(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         subject = "Invitation for hackFMI membership"
#         body = faker.paragraph()

#         msg = EmailMultiAlternatives(subject=subject,
#                                      body=body,
#                                      from_email=settings.DJANGO_DEFAULT_FROM_EMAIL,
#                                      to=[competitor.email])

#         response = msg.send()

#         self.assertEqual(response, 1)

#     def test_non_leaders_cant_send_invitations(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=competitor,
#             team=team,
#             is_leader=False,
#         )
#         self.client.force_authenticate(user=competitor)

#         url = reverse('hack_fmi:invitation-list')
#         data = {'competitor_email': faker.word() + faker.email()}
#         response = self.client.post(url, data,)

#         self.response_403(response)

#     def test_send_invitation_to_not_existing_user(self):
#         """
#         Every time a test is run, SeasonFactory generates random max_team_members_count.
#         That's why we intentionaly specifi max_team_members_count.
#         """
#         self.season.max_team_members_count = 2
#         self.season.save()

#         recipient = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=recipient,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(user=recipient)

#         url = reverse('hack_fmi:invitation-list')
#         data = {'competitor_email': faker.word() + faker.email()}
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_send_invitation_twice_to_same_competitor(self):
#         recipient = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=recipient,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(user=recipient)

#         Invitation.objects.create(
#             team=team,
#             competitor=recipient,
#         )
#         url = reverse('hack_fmi:invitation-list')
#         data = {'competitor_email': recipient.email}
#         response = self.client.post(url, data)

#         self.response_403(response)

#     def test_send_invitation_when_team_is_full(self):
#         self.season.max_team_members_count = 2
#         self.season.save()

#         recipient = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=recipient,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(user=recipient)

#         competitor2 = factories.CompetitorFactory(
#             email=faker.email()
#         )

#         factories.TeamMembershipFactory(
#             competitor=competitor2,
#             team=team,
#             is_leader=False,
#         )

#         self.assertEqual(TeamMembership.objects.filter(team=team).count(), 2)

#         url = reverse('hack_fmi:invitation-list')
#         data = {'competitor_email': recipient.email}

#         response = self.client.post(url, data)

#         self.response_403(response)
#         self.assertEqual(TeamMembership.objects.filter(team=team).count(), 2)

#     def test_user_cant_get_his_invitations_if_not_being_hackfmi_user(self):
#         user = factories.BaseUserFactory(
#             email=faker.email()
#         )
#         self.client.force_authenticate(user=user)

#         url = reverse('hack_fmi:invitation-list')
#         response = self.client.get(url)

#         self.response_403(response)

#     def test_user_can_get_his_invitations_if_hackfmi_user(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.InvitationFactory(
#             team=team,
#             competitor=competitor
#         )
#         self.client.force_authenticate(user=competitor)

#         url = reverse('hack_fmi:invitation-list')
#         response = self.client.get(url)

#         self.response_200(response)
#         self.assertEqual(len(response.data), 1)

#     def test_send_invitation_to_user_that_already_has_team(self):
#         recipient = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         receiver = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         factories.TeamMembershipFactory(
#             competitor=recipient,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(user=recipient)

#         receiver_team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )

#         factories.TeamMembershipFactory(
#             team=receiver_team,
#             competitor=receiver,
#         )

#         url = reverse('hack_fmi:invitation-list')
#         data = {
#             'competitor_email': receiver.email
#         }
#         response = self.client.post(url, data)

#         self.response_403(response)

#     def test_accept_invitation(self):
#         competitor_not_leader = factories.CompetitorFactory(
#             email=faker.email(),
#         )
#         team = factories.TeamFactory(
#             name=faker.name(),
#             season=self.season,
#         )
#         self.client.force_authenticate(user=competitor_not_leader)

#         inv = factories.InvitationFactory(
#             team=team,
#             competitor=competitor_not_leader
#         )
#         url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

#         response = self.client.post(url)
#         self.response_200(response)
#         self.assertEqual(Invitation.objects.all().count(), 0)
#         self.\
#             assertTrue(TeamMembership.objects.filter(team=inv.team, competitor=inv.competitor).exists())

#     def test_accept_invitation_already_has_team(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             season=self.season
#         )
#         factories.TeamMembershipFactory(
#             competitor=competitor,
#             team=team,
#         )

#         inv = factories.InvitationFactory(
#             team=team,
#             competitor=competitor
#         )
#         self.client.force_authenticate(user=competitor)

#         url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

#         response = self.client.post(url)

#         self.response_403(response)

#     def test_can_not_accept_invitation_to_other_team_if_you_are_a_leader(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             season=self.season
#         )
#         factories.TeamMembershipFactory(
#             competitor=competitor,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(competitor)

#         inv = factories.InvitationFactory(
#             team=team,
#             competitor=competitor
#         )

#         url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

#         response = self.client.post(url)

#         self.response_403(response)

#     def test_accept_invitation_that_is_not_yours(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         self.client.force_authenticate(user=competitor)

#         other_competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             season=self.season
#         )
#         inv = factories.InvitationFactory(
#             team=team,
#             competitor=other_competitor
#         )

#         url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

#         response = self.client.post(url)

#         self.response_403(response)

#     def test_decline_invitation_if_you_are_already_a_member_in_other_team(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             season=self.season
#         )
#         factories.TeamMembershipFactory(
#             competitor=competitor,
#             team=team,
#             is_leader=True,
#         )
#         self.client.force_authenticate(competitor)

#         factories.TeamMembershipFactory(
#             team=team,
#             competitor=competitor,
#         )

#         invitation = factories.InvitationFactory(
#             team=team,
#             competitor=competitor
#         )
#         self.assertEqual(Invitation.objects.all().count(), 1)

#         url = reverse('hack_fmi:invitation-detail', kwargs={'pk': invitation.id})
#         response = self.client.delete(url)

#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Invitation.objects.all().count(), 0)

#     def test_decline_invitation_that_is_not_yours(self):
#         competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )

#         other_competitor = factories.CompetitorFactory(
#             email=faker.email()
#         )
#         team = factories.TeamFactory(
#             season=self.season
#         )
#         self.client.force_authenticate(user=competitor)

#         invitation = factories.InvitationFactory(
#             team=team,
#             competitor=other_competitor
#         )
#         self.assertEqual(Invitation.objects.all().count(), 1)
#         url = reverse('hack_fmi:invitation-detail', kwargs={'pk': invitation.id})

#         response = self.client.delete(url)

#         self.response_403(response)
#         self.assertFalse(TeamMembership.objects.filter(competitor=invitation.competitor).exists())
#         self.assertEqual(Invitation.objects.all().count(), 1)


class TeamMentorshipAPITest(TestCase):

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
class RoomTests(TestCase):

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
