from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import (Skill, Competitor, BaseUser, TeamMembership,
                     Season, Team, Invitation)


class SkillTests(APITestCase):

    def setUp(self):
        self.skill = Skill.objects.create(name="C#")

    def test_get_skill(self):
        url = reverse('hack_fmi:skills')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegistrationTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")

    def test_register_user(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': [self.skills.id],
            'password': '123',
            'needs_work': 'false',
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)
        self.assertEqual(len(Competitor.objects.first().known_skills.all()), 1)
        self.assertFalse(Competitor.objects.first().needs_work)

    def test_register_user_no_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': [self.skills.id],
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sent(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'faculty_number': '123',
            'known_skills': [self.skills.id],
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_sent_new_template(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'faculty_number': '123',
            'known_skills': [self.skills.id],
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Ти успешно се регистрира за HackFMI 5! През нашата нова система можеш лесно да намериш отбор, с който да се състезаваш.  Ако вече имаш идея можеш да създадеш отбор и да поканиш още хора в него.", mail.outbox[0].body)


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

    def test_login(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123321',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_not_competitor(self):
        self.base_user = BaseUser.objects.create(
            email='baseuser@abv.bg',
            full_name='Ivo Naidobriq',
        )
        self.base_user.set_password('123')
        self.base_user.save()

        data = {
            'email': 'baseuser@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_data_after_login(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.competitor.email)

    def test_get_data_not_login(self):
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeamRegistrationTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.season = Season.objects.create(number=1, is_active=True)
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.team_data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': [self.skills.id]
        }
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)

    def test_register_team(self):
        url = reverse('hack_fmi:register_team')
        response = self.client.post(url, self.team_data, format='json')
        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['technologies']), 1)

    def test_registered_team_has_leader(self):
        url = reverse('hack_fmi:register_team')
        self.client.post(url, self.team_data, format='json')
        team_membership = TeamMembership.objects.first()
        self.assertEqual(self.competitor, team_membership.competitor)
        self.assertTrue(team_membership.is_leader)

    # def test_register_more_than_one_team(self):
    #     url = reverse('hack_fmi:register_team')
    #     first_response = self.client.post(url, self.team_data, format='json')

    #     data = {
    #         'name': 'Pandass',
    #         'idea_description': 'GameDeveloperss',
    #         'repository': 'https://github.com/HackSoftwares',
    #         'technologies': [self.skills.id],
    #     }
    #     url = reverse('hack_fmi:register_team')
    #     second_response = self.client.post(url, data, format='json')
    #     self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Team.objects.count(), 1)


class TeamManagementTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.season = Season.objects.create(number=1, is_active=True)
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)

    def test_list_team_by_id(self):
        team1 = Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        team2 = Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        url_get = reverse('hack_fmi:teams')
        data = {'id': team2.id}
        response = self.client.get(url_get, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Pandass2')

    def test_list_team_all(self):
        Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        url_get = reverse('hack_fmi:teams')
        response = self.client.get(url_get, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_invitation_for_team(self):
        data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': [self.skills.id],
        }
        url = reverse('hack_fmi:register_team')
        self.client.post(url, data, format='json')
        team = Team.objects.first()
        self.competitor2 = Competitor.objects.create(
            email='stenly@abv.bg',
            full_name='Stenly Naidobriq',
            faculty_number='1234',
        )
        url = reverse('hack_fmi:invitation')
        data = {'email': 'stenly@abv.bg'}
        self.client.post(url, data, format='json')
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.all()[0].team.id, team.id)
        self.assertEqual(Invitation.objects.all()[0].competitor.id, self.competitor2.id)

    def test_test_invitation_not_from_leader(self):
        Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        url = reverse('hack_fmi:invitation')
        data = {'email': 'stenly@abv.bg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invitations(self):
        team = Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        Invitation.objects.create(
            team=team,
            competitor=self.competitor
        )
        url = reverse('hack_fmi:invitation')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_accept_invitations(self):
        team = Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        invitation = Invitation.objects.create(
            team=team,
            competitor=self.competitor
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(TeamMembership.objects.all()), 1)
        self.assertEqual(len(Invitation.objects.all()), 0)

    # def test_accept_decline(self):
    #     team = Team.objects.create(
    #         name='Pandass2',
    #         idea_description='GameDevelopers',
    #         repository='https://github.com/HackSoftware',
    #         season=self.season
    #     )
    #     invitation = Invitation.objects.create(
    #         team=team,
    #         competitor=self.competitor
    #     )
    #     url = reverse('hack_fmi:invitation')
    #     data = {'id': invitation.id}
    #     response = self.client.delete(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(TeamMembership.objects.all()), 0)
    #     self.assertEqual(len(Invitation.objects.all()), 0)


class LeaveTeamTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.season = Season.objects.create(number=1, is_active=True)
        self.competitor1 = Competitor.objects.create(
            email='ivooo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
            is_active=True,
        )
        self.competitor2 = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivooo Naidobriq',
            faculty_number='124',
            is_active=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor1)
        data = {
            'name': 'Pandass',
            'idea_description': 'GameDeveloperss',
            'repository': 'https://github.com/HackSoftwares',
            'technologies': [self.skills.id],
        }
        url = reverse('hack_fmi:register_team')
        self.client.post(url, data, format='json')
        self.team = Team.objects.first()
        TeamMembership.objects.create(competitor=self.competitor2, team=self.team)

    def test_member_leaves_team(self):
        self.client.logout()
        self.client.force_authenticate(user=self.competitor2)
        self.assertEqual(self.team.members.count(), 2)
        url = reverse('hack_fmi:leave_team')
        self.client.post(url, format='json')
        self.assertEqual(self.team.members.count(), 1)

    def test_leader_leaves_team(self):
        url = reverse('hack_fmi:leave_team')
        self.assertEqual(self.team.members.count(), 2)
        self.client.post(url, format='json')

        self.assertEqual(self.team.members.count(), 0)
        self.assertEqual(len(Team.objects.all()), 0)
        self.assertEqual(len(TeamMembership.objects.all()), 0)

    def test_leader_leaves_team_emails_sent(self):
        url = reverse('hack_fmi:leave_team')
        self.client.post(url, format='json')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 2)
