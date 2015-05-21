from django.core.management.base import CommandError
from django.core.management import call_command
from django.core.urlresolvers import reverse
from post_office import mail

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from post_office.models import EmailTemplate

from .models import (Skill, Competitor, BaseUser, TeamMembership,
                     Season, Team, Invitation, Mentor, Room)


class SkillTests(APITestCase):

    def setUp(self):
        self.skill = Skill.objects.create(name="C#")

    def test_get_skill(self):
        url = reverse('hack_fmi:skills')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PasswordResetTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.password_reset = EmailTemplate.objects.create(
            name='password_reset',
            subject='Смяна на Парола',
            content='Lorem ipsum dolor sit amet, consectetur adipisicing'
        )
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.competitor.set_password('123')
        self.competitor.is_active = True
        self.competitor.save()

    def test_reset_password_sends_email(self):
        data = {'email': 'ivo@abv.bg'}
        url = reverse('hack_fmi:password_reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.get_queued()), 1)
        self.assertIn(self.password_reset.content, mail.get_queued()[0].message)


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
        self.base_user.is_active = True
        self.base_user.save()

        data = {
            'email': 'baseuser@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.season = Season.objects.create(
            name="season",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1"
        )
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
        url = reverse('hack_fmi:teams')
        response = self.client.post(url, self.team_data, format='json')
        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['technologies']), 1)
        self.assertEqual(len(response.data['technologies_full']), 1)

    def test_registered_team_has_leader(self):
        url = reverse('hack_fmi:teams')
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
        self.season = Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1"
        )

        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)

    def test_list_team_by_id(self):
        Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season,
        )
        team2 = Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )

        url_get = reverse('hack_fmi:teams', kwargs={
            'pk': team2.id,
        })

        response = self.client.get(url_get, format='json')
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

    def test_update_test(self):
        team = Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        team.add_member(self.competitor, is_leader=True)

        data = {
            'name': 'New panda name',
        }

        url_get = reverse('hack_fmi:teams', kwargs={
                'pk': team.id,
            }
        )
        response = self.client.patch(url_get, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Team.objects.first().name, data['name'])

    def test_update_not_leader(self):
        team = Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season
        )
        team.add_member(self.competitor, is_leader=False)

        data = {
            'name': 'New panda name',
        }

        url_get = reverse('hack_fmi:teams', kwargs={
                'pk': team.id,
            }
        )
        response = self.client.patch(url_get, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.first().name, 'Pandass')

    def test_create_team(self):
        self.season.is_active = False

        self.season2 = Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )

        data = {
            'name': 'Team name',
            'idea_description': 'lorem',
            'technologies': [self.skills.id]
        }

        url_get = reverse('hack_fmi:teams')
        response = self.client.post(url_get, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        team = Team.objects.get(name="Team name")

        self.assertEqual(team.season, self.season2)


class LeaveTeamTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.template = EmailTemplate.objects.create(
            name='delete_team',
            subject='Изтрит отбор HackFMI',
            content='Лидера на твоя отбор напусна и отбора беше изтрит.',
        )
        self.season = Season.objects.create(
            name="HackFMI 10",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
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
        url = reverse('hack_fmi:teams')
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

        self.assertEqual(len(mail.get_queued()), 1)
        self.assertEqual(len(mail.get_queued()[0].to), 2)


class InvitationTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.season = Season.objects.create(
            name="HackFMI 2",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
        self.competitor_leader = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.competitor_not_leader = Competitor.objects.create(
            email='sten@abv.bg',
            full_name='Sten Naidobriq',
            faculty_number='123',
        )
        self.competitor_dummy = Competitor.objects.create(
            email='dummy@abv.bg',
            full_name='Dummy Naidobriq',
            faculty_number='123',
        )
        self.team = Team.objects.create(
            name='Pandas',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season,
        )
        self.team_dummy = Team.objects.create(
            name='Dummy',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season,
        )
        self.team_membership = TeamMembership.objects.create(
            competitor=self.competitor_leader,
            team=self.team,
            is_leader=True,
        )

    def test_send_invitation_for_team(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        url = reverse('hack_fmi:invitation')
        data = {'email': self.competitor_not_leader.email}
        self.client.post(url, data, format='json')

        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.all()[0].team.id, self.team.id)
        self.assertEqual(Invitation.objects.all()[0].competitor.id, self.competitor_not_leader.id)

    def test_test_send_invitation_not_from_leader(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_not_leader)
        TeamMembership.objects.create(
            competitor=self.competitor_not_leader,
            team=self.team,
            is_leader=False,
        )

        url = reverse('hack_fmi:invitation')
        data = {'email': self.competitor_dummy.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_invitation_to_not_existing_user(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        url = reverse('hack_fmi:invitation')
        data = {'email': 'not_exist@abv.bg'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_invitation_twice_to_same_competitor(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'email': self.competitor_not_leader.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_invitation_member_already_in_team(self):
        TeamMembership.objects.create(
            competitor=self.competitor_not_leader,
            team=self.team,
            is_leader=False,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        url = reverse('hack_fmi:invitation')
        data = {'email': self.competitor_not_leader.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_invitation_when_team_is_full(self):
        for i in range(5):
            TeamMembership.objects.create(
                competitor=Competitor.objects.create(
                    email='dummy{0}@abv.bg'.format(i),
                    full_name='Dum Naidobriq',
                    faculty_number='123',
                ),
                team=self.team,
                is_leader=False,
            )
        self.assertEqual(self.team.members.count(), 6)
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        url = reverse('hack_fmi:invitation')
        data = {'email': self.competitor_not_leader.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invitations(self):
        Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_not_leader)

        url = reverse('hack_fmi:invitation')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_accept_invitation(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_not_leader)
        invitation = Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(TeamMembership.objects.all()), 2)
        self.assertEqual(len(Invitation.objects.all()), 0)

    def test_accept_invitation_already_has_team(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_not_leader)
        TeamMembership.objects.create(
            competitor=self.competitor_not_leader,
            team=self.team_dummy,
            is_leader=True,
        )
        invitation = Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_invitation_that_is_not_yours(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)

        invitation = Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_decline_invitation(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_not_leader)
        invitation = Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(TeamMembership.objects.all()), 1)
        self.assertEqual(len(Invitation.objects.all()), 0)

    def test_decline_invitation_that_is_not_yours(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)
        invitation = Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation')
        data = {'id': invitation.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(TeamMembership.objects.all()), 1)
        self.assertEqual(len(Invitation.objects.all()), 1)


class SeasonTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic1',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-15",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
        Season.objects.create(
            name="HackFMI 2",
            topic='TestTopic2',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2016-4-15",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )

    def test_season_deactivates_automatically(self):
        self.assertFalse(Season.objects.get(name="HackFMI 1").is_active)

    def test_get_season(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:season')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MentorTests(APITestCase):

    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        # TODO: Fix dates not to be hardcoded
        self.season = Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2016-5-1",
            mentor_pick_start_date="2015-4-1",
            mentor_pick_end_date="2016-5-1",
            make_team_dead_line="2016-5-1",
        )
        self.competitor_leader = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.team = Team.objects.create(
            name='Pandas',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.season,
        )
        self.team_membership = TeamMembership.objects.create(
            competitor=self.competitor_leader,
            team=self.team,
            is_leader=True,
        )
        self.mentor = Mentor.objects.create(
            name='Sten',
            description='I help!',
        )
        self.mentor2 = Mentor.objects.create(
            name='Sten2',
            description='I help!',
        )

    def test_get_mentors(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)
        url = reverse('hack_fmi:mentors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_mentor_to_leader_team(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)
        url = reverse('hack_fmi:assign_mentor')
        data = {'id': self.mentor.id, 'team_id': self.team.id}
        self.client.put(url, data, format='json')
        name = self.team.mentors.get(id=self.mentor.id)
        self.assertEqual(str(name), "Sten")

    def test_assign_more_than_allowed_mentors(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)
        url = reverse('hack_fmi:assign_mentor')
        data = {'id': self.mentor.id, 'team_id': self.team.id}
        self.client.put(url, data, format='json')
        data = {'id': self.mentor2.id, 'team_id': self.team.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_mentor_after_endtime(self):
        self.season.mentor_pick_end_date = "2013-5-1"
        self.season.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor_leader)
        url = reverse('hack_fmi:assign_mentor')
        data = {'id': self.mentor.id, 'team_id': self.team.id}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RoomTests(APITestCase):

    def setUp(self):
        self.season = Season.objects.create(
            name="HackFMI 1",
            topic='TestTopic',
            is_active=True,
            sign_up_deadline="2015-5-1",
            mentor_pick_start_date="2015-4-1",
            mentor_pick_end_date="2015-5-1",
            make_team_dead_line="2016-5-1",
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
                number=100+i,
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
                name='Pandas{0}'.format(i+15),
                idea_description='GameDevelopers',
                repository='https://github.com/HackSoftware',
                season=self.season,
            )
        with self.assertRaises(CommandError):
            call_command('fillrooms')
