from django.core.management.base import CommandError
from django.core.management import call_command
from django.core.urlresolvers import reverse
from post_office import mail
from django.db import IntegrityError

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from test_plus.test import TestCase
from post_office.models import EmailTemplate

from ..helper import date_increase, date_decrease
from ..models import (Skill, Competitor, TeamMembership,
                      Season, Team, Invitation, Mentor, Room,
                      TeamMentorship)
import unittest

from seed import factories

from faker import Factory

faker = Factory.create()


class SkillTests(TestCase):

    def setUp(self):
        self.skill = factories.SkillFactory()

    def test_get_skill(self):
        url = reverse('hack_fmi:skills')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MentorListAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.student = factories.StudentFactory(
            email=faker.email()
        )
        self.company = factories.HackFmiPartnerFactory()
        self.active_season = factories.SeasonFactory(
            is_active=True)

        self.non_active_season = factories.SeasonFactory(
            is_active=False)

        self.mentor = factories.MentorFactory(
            from_company=self.company
        )
        self.active_season.mentor_set.add(self.mentor)
        self.active_season.save()

        self.mentor2 = factories.MentorFactory(
            from_company=self.company
        )
        self.non_active_season.mentor_set.add(self.mentor2)
        self.non_active_season.save()

        self.mentor3 = factories.MentorFactory(
            from_company=self.company
        )
        self.active_season.mentor_set.add(self.mentor3)
        self.active_season.save()

    def test_get_mentor_for_active_season(self):
        self.client.force_authenticate(self.student)
        url = reverse('hack_fmi:mentors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.mentor.name)

    def test_get_active_mentors_from_active_season(self):
        self.client.force_authenticate(self.student)
        url = reverse('hack_fmi:mentors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        active_seasons = Season.objects.filter(is_active=True)
        self.assertEqual(active_seasons[0].mentor_set.count(), 2)


class SeasonListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(
            from_company=self.company
        )
        self.active_season = factories.SeasonFactory(
            is_active=True)

        self.non_active_season = factories.SeasonFactory(
            is_active=False)

    def test_get_active_season(self):
        url = reverse('hack_fmi:season')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.active_season.name)
        self.assertEqual(Season.objects.filter(is_active=True).count(), 1)


class PublicTeamViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.active_season = factories.SeasonFactory(
            is_active=True)

        self.room = factories.RoomFactory(season=self.active_season)

        self.team = factories.TeamFactory(
            season=self.active_season,
            room=self.room)

    def get_team_from_active_season(self):
        url = reverse('hack_fmi:public_teams')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.team.name)

    def get_team_from_non_active_season(self):
        url = reverse('hack_fmi:public_teams')

        non_active_season = factories.SeasonFactory(
            is_active=False)
        non_active_team = factories.TeamFactory(season=non_active_season)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]['name'], non_active_team.name)


class TeamAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(
            is_active=True,
            make_team_dead_line=date_decrease(30),
            max_mentor_pick=100,
        )

        self.non_active_season = factories.SeasonFactory(
            is_active=False)

        self.room = factories.RoomFactory(season=self.active_season)

        self.team = factories.TeamFactory(
            season=self.active_season,
            room=self.room)

        self.non_active_team = factories.TeamFactory(
            season=self.non_active_season,
            room=self.room)

        self.competitor = factories.CompetitorFactory(
            email=faker.email()
        )

        self.competitor2 = factories.CompetitorFactory(
            email=faker.email()
        )

        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(
            from_company=self.company)

    def test_get_team_without_IsHackFMIUser_permission(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        url = reverse('hack_fmi:teams')

        response = self.client.get(url, kwargs={'pk': faker.random_number(digits=1)})

        self.response_401(response)

    def test_get_team_with_IsHackFMIUser_IsTeamInActiveSeason_IsSeasonDeadlineUpToDate_permissions(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)
        url = reverse('hack_fmi:teams')

        response = self.client.get(url, kwargs={'pk': self.team.id})

        self.response_200(response)

    def test_get_team_without_IsTeamLeader_permission(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=False,
        )
        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:teams')

        response = self.client.get(url, kwargs={'pk': self.team.id})

        self.response_200(response)

    def test_change_team_without_IsTeamLeader_permission(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=False,
        )
        self.client.force_authenticate(self.competitor)
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': self.team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_change_team_with_IsTeamLeader_permission(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': self.team.id})

        response = self.client.patch(url, data)

        self.response_200(response)
        self.assertIsNotNone(Team.objects.get(name=data['name']))
        self.assertIsNotNone(Team.objects.get(idea_description=data['idea_description']))

    def test_get_team_of_non_active_season_with_pk(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.non_active_team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)
        url = reverse('hack_fmi:teams', kwargs={'pk': self.non_active_team.id})

        response = self.client.get(url)

        self.response_200(response)

    def test_change_team_of_non_active_season_with_pk(self):
        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.non_active_team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': self.non_active_team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_get_team_with_IsSeasonDeadlineUpToDate_permission(self):
        self.active_season.make_team_dead_line = date_increase(100)
        self.active_season.save()

        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.client.force_authenticate(self.competitor)
        url = reverse('hack_fmi:teams', kwargs={'pk': self.team.id})

        response = self.client.get(url)

        self.response_200(response)

    def test_change_team_without_IsSeasonDeadlineUpToDate_permission(self):
        self.active_season.make_team_dead_line = date_increase(100)
        self.active_season.save()

        factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:teams', kwargs={'pk': self.team.id})

        response = self.client.patch(url, data)

        self.response_403(response)


class TeamMembershipAPITest(TestCase):

    def setUp(self):
        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(
            from_company=self.company)
        self.client = APIClient()

        self.active_season = factories.SeasonFactory(
            is_active=True
        )
        self.non_active_season = factories.SeasonFactory(
            is_active=False)

        self.room = factories.RoomFactory(
            season=self.active_season)
        self.team = factories.TeamFactory(
            season=self.active_season,
        )
        self.non_active_team = factories.TeamFactory(
            season=self.non_active_season)

        self.competitor = factories.CompetitorFactory(
            email=faker.email())
        self.delete_team = EmailTemplate.objects.create(
            name='delete_team',
            subject='Delete team',
            content=faker.paragraph()
        )

    def test_delete_team_membership_if_not_member_of_team(self):
        other_competitor = factories.CompetitorFactory(
            email=faker.email())
        other_membership = factories.TeamMembershipFactory(
            competitor=other_competitor,
            team=self.team,
            is_leader=True,
        )
        my_membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=False,
        )
        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': other_membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_delete_team_membership_if_not_hack_fmi_user(self):
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

    def test_delete_team_membership_if_not_active_season(self):
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.non_active_team,
            is_leader=True,
        )

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_delete_team_membership_if_competitor_not_teamleader(self):
        membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=False,
        )

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(Team.objects.filter(name=self.team.name).count(), 1)
        self.assertEqual(TeamMembership.objects.filter(competitor=self.competitor).count(), 0)

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

        self.client.force_authenticate(self.competitor)

        url = reverse('hack_fmi:team_membership', kwargs={'pk': membership.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.filter(name=team.name).count(), 0)
        self.assertEqual(TeamMembership.objects.filter(competitor=self.competitor).count(), 0)


# @unittest.skip('Skip until further implementation of Hackathon system')
# class TeamRegistrationTests(TestCase):

#     def setUp(self):
#         self.skills = Skill.objects.create(name="C#")
#         self.season = Season.objects.create(
#             name="season",
#             topic='TestTopic',
#             is_active=True,
#             sign_up_deadline=date_increase(10),
#             mentor_pick_start_date=date_increase(15),
#             mentor_pick_end_date=date_increase(25),
#             make_team_dead_line=date_increase(20)
#         )
#         self.competitor = Competitor.objects.create(
#             email='ivo@abv.bg',
#             full_name='Ivo Naidobriq',
#             faculty_number='123',
#         )
#         self.team_data = {
#             'name': 'Pandas',
#             'idea_description': 'GameDevelopers',
#             'repository': 'https://github.com/HackSoftware',
#             'technologies': [self.skills.id]
#         }
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.competitor)

#     def test_register_team(self):
#         url = reverse('hack_fmi:teams')
#         response = self.client.post(url, self.team_data, format='json')
#         self.assertEqual(len(response.data['members']), 1)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(response.data['technologies']), 1)
#         self.assertEqual(len(response.data['technologies_full']), 1)

#     def test_registered_team_has_leader(self):
#         url = reverse('hack_fmi:teams')
#         self.client.post(url, self.team_data, format='json')
#         team_membership = TeamMembership.objects.first()
#         self.assertEqual(self.competitor, team_membership.competitor)
#         self.assertTrue(team_membership.is_leader)

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


class InvitationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.template = EmailTemplate.objects.create(
            name='hackfmi_team_invite',
            subject='Покана за отбор във HackFMI',
            content='Покана за отбор във HackFMI.',
        )

        self.season = factories.SeasonFactory(
            is_active=True,
            max_team_members_count=3,
        )
        self.competitor = factories.CompetitorFactory(
            email=faker.email(),
        )
        self.competitor_not_leader = factories.CompetitorFactory(
            email=faker.email(),
        )
        self.team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        self.team_membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )

    def test_send_invitation_for_team(self):
        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:invitation')
        data = {'competitor_email': self.competitor_not_leader.email}
        response = self.client.post(url, data)

        self.response_201(response)
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEqual(Invitation.objects.all()[0].team.id, self.team.id)
        self.assertEqual(Invitation.objects.all()[0].competitor.id, self.competitor_not_leader.id)

    def test_send_invitation_not_from_leader(self):
        competitor = factories.CompetitorFactory(
            email=faker.email(),
        )

        factories.TeamMembershipFactory(
            competitor=competitor,
            team=self.team,
            is_leader=False,
        )
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:invitation')
        data = {'competitor_email': self.competitor_not_leader.email}
        response = self.client.post(url, data,)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_invitation_to_not_existing_user(self):
        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:invitation')
        data = {'competitor_email': faker.email()}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_invitation_twice_to_same_competitor(self):
        self.client.force_authenticate(user=self.competitor)

        Invitation.objects.create(
            team=self.team,
            competitor=self.competitor_not_leader,
        )
        url = reverse('hack_fmi:invitation')
        data = {'competitor_email': self.competitor_not_leader.email}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_invitation_when_team_is_full(self):
        self.client.force_authenticate(user=self.competitor)

        competitor2 = factories.CompetitorFactory(
            email=faker.email()
        )
        competitor3 = factories.CompetitorFactory(
            email=faker.email()
        )

        factories.TeamMembershipFactory(
            competitor=competitor2,
            team=self.team,
            is_leader=False,
        )
        factories.TeamMembershipFactory(
            competitor=competitor3,
            team=self.team,
            is_leader=False,
        )
        self.assertEqual(TeamMembership.objects.filter(team=self.team).count(), 3)

        url = reverse('hack_fmi:invitation')
        data = {'competitor_email': self.competitor_not_leader.email}

        response = self.client.post(url, data)

        self.response_403(response)
        self.assertEqual(TeamMembership.objects.filter(team=self.team).count(), 3)

    def test_get_invitations_if_not_hackFMI_user(self):
        user = factories.BaseUserFactory(
            email=faker.email()
        )
        self.client.force_authenticate(user=user)

        url = reverse('hack_fmi:invitation')
        response = self.client.get(url)

        self.response_403(response)

    def test_get_invitations_if_not_leader_and_hackFMI_user(self):
        factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        self.client.force_authenticate(user=self.competitor_not_leader)

        url = reverse('hack_fmi:invitation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_invitations_if_leader_and_hackFMI_user(self):
        factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor
        )
        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:invitation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Invitation.objects.all().count(), 1)

    def test_send_invitation_to_user_that_already_has_team(self):
        self.client.force_authenticate(self.competitor)

        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )

        factories.TeamMembershipFactory(
            team=team,
            competitor=self.competitor_not_leader,
        )

        url = reverse('hack_fmi:invitation')
        data = {
            'competitor_email': self.competitor_not_leader.email
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_accept_invitation(self):
    #     self.client.force_authenticate(user=self.competitor_not_leader)

    #     inv = factories.InvitationFactory(
    #         team=self.team,
    #         competitor=self.competitor_not_leader
    #     )
    #     url = reverse('hack_fmi:invitation')
    #     data = {'id': inv.id}

    #     response = self.client.put(url, data)
    #     self.response_200(response)
    #     self.assertEqual(Invitation.objects.all().count(), 0)
    #     self.\
    #         assertEqual(TeamMembership.objects.filter(team=inv.team, competitor=inv.competitor).count(), 1)

    # def test_accept_invitation_already_has_team(self):
    #     team = factories.TeamFactory(
    #         season=self.season
    #     )
    #     factories.TeamMembershipFactory(
    #         competitor=self.competitor_not_leader,
    #         team=team,
    #     )

    #     invitation = factories.InvitationFactory(
    #         team=team,
    #         competitor=self.competitor_not_leader
    #     )
    #     self.client.force_authenticate(user=self.competitor_not_leader)

    #     url = reverse('hack_fmi:invitation')
    #     data = {'id': invitation.id}

    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_accept_invitation_that_is_not_yours(self):
    #     self.client.force_authenticate(user=self.competitor)

    #     invitation = factories.InvitationFactory(
    #         team=self.team,
    #         competitor=self.competitor_not_leader
    #     )

    #     url = reverse('hack_fmi:invitation')
    #     data = {'id': invitation.id}

    #     response = self.client.put(url, data)
    #     self.response_403(response)
    def test_decline_non_confirmed_invitation_if_leader(self):
        self.client.force_authenticate(user=self.competitor)

        invitation = factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        url = reverse('hack_fmi:invitation', kwargs={'pk': invitation.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_decline_confirmed_invitation_if_leader(self):
        self.client.force_authenticate(user=self.competitor)

        factories.TeamMembershipFactory(
            team=self.team,
            competitor=self.competitor_not_leader,
        )

        invitation = factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )

        self.assertEqual(TeamMembership.objects.filter(team=invitation.team, competitor=invitation.competitor).count(), 1)
        self.assertEqual(Invitation.objects.all().count(), 1)

        url = reverse('hack_fmi:invitation', kwargs={'pk': invitation.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMembership.objects.filter(team=invitation.team, competitor=invitation.competitor).count(), 0)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_decline_confirmed_invitation_if_not_leader(self):
        self.client.force_authenticate(user=self.competitor_not_leader)

        factories.TeamMembershipFactory(
            team=self.team,
            competitor=self.competitor_not_leader,
        )

        invitation = factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        self.assertEqual(TeamMembership.objects.filter(team=invitation.team, competitor=invitation.competitor).count(), 1)
        self.assertEqual(Invitation.objects.all().count(), 1)

        url = reverse('hack_fmi:invitation', kwargs={'pk': invitation.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMembership.objects.filter(team=invitation.team, competitor=invitation.competitor).count(), 0)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_decline_non_confirmed_invitation_if_not_leader(self):
        self.client.force_authenticate(user=self.competitor_not_leader)

        invitation = factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        self.assertEqual(Invitation.objects.all().count(), 1)

        url = reverse('hack_fmi:invitation', kwargs={'pk': invitation.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMembership.objects.filter(team=invitation.team, competitor=invitation.competitor).count(), 0)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_decline_invitation_that_is_not_yours(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )

        self.client.force_authenticate(user=competitor)

        invitation = factories.InvitationFactory(
            team=self.team,
            competitor=self.competitor_not_leader
        )
        self.assertEqual(Invitation.objects.all().count(), 1)
        url = reverse('hack_fmi:invitation', kwargs={'pk': invitation.id})

        response = self.client.delete(url)

        self.response_403(response)
        self.assertEqual(TeamMembership.objects.filter(competitor=invitation.competitor).count(), 0)
        self.assertEqual(Invitation.objects.all().count(), 1)


# @unittest.skip('Skip until further implementation of Hackathon system')
# class SeasonTests(APITestCase):

#     def setUp(self):
#         self.skills = Skill.objects.create(name="C#")
#         Season.objects.create(
#             name="HackFMI 1",
#             topic='TestTopic1',
#             is_active=True,
#             sign_up_deadline=date_increase(10),
#             mentor_pick_start_date=date_increase(15),
#             mentor_pick_end_date=date_increase(25),
#             make_team_dead_line=date_increase(20),
#         )
#         Season.objects.create(
#             name="HackFMI 2",
#             topic='TestTopic2',
#             is_active=True,
#             sign_up_deadline=date_increase(10),
#             mentor_pick_start_date=date_increase(15),
#             mentor_pick_end_date=date_increase(25),
#             make_team_dead_line=date_increase(20),
#         )
#         self.competitor = Competitor.objects.create(
#             email='ivo@abv.bg',
#             full_name='Ivo Naidobriq',
#             faculty_number='123',
#         )

#     def test_season_deactivates_automatically(self):
#         self.assertFalse(Season.objects.get(name="HackFMI 1").is_active)

#     def test_get_season(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.competitor)
#         url = reverse('hack_fmi:season')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamMentorshipTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.skills = factories.SkillFactory()

        self.season = factories.SeasonFactory(
            is_active=True,
            # max_mentor_pick=1,
        )
        self.competitor = factories.CompetitorFactory(
            email=faker.email(),
        )
        self.team = factories.TeamFactory(
            season=self.season,
        )
        self.team_membership = factories.TeamMembershipFactory(
            competitor=self.competitor,
            team=self.team,
            is_leader=True,
        )
        self.company = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(
            from_company=self.company,
        )
        self.mentor2 = factories.MentorFactory(
            from_company=self.company,
        )

    def test_assign_mentor_if_not_hackFMI_user(self):
        competitor = factories.CompetitorFactory(
            email=faker.email(),)

        self.client.force_authenticate(competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_mentor_if_not_leader_team(self):
        self.team.season.mentor_pick_start_date = date_decrease(10)
        self.team.season.mentor_pick_end_date = date_increase(10)
        self.team.save()

        self.team_membership.is_leader = False
        self.team_membership.save()

        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        response = self.client.post(url, data)

        self.response_403(response)

    # def test_assign_more_than_allowed_mentors(self):
    #     self.client.force_authenticate(user=self.competitor)

    #     url = reverse('hack_fmi:team_mentorship')

    #     data = {'id': self.mentor.id, 'team_id': self.team.id}
    #     self.client.put(url, data)

    #     data = {'id': self.mentor2.id, 'team_id': self.team.id}

    #     response = self.client.put(url, data)

    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_mentor_before_startdate(self):
        self.team.season.mentor_pick_start_date = date_increase(10)
        self.team.season.mentor_pick_end_date = date_increase(10)
        self.team.season.save()

        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }
        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_mentor_after_enddate(self):
        self.team.season.mentor_pick_start_date = date_decrease(10)
        self.team.season.mentor_pick_end_date = date_decrease(10)
        self.team.season.save()

        self.client.force_authenticate(user=self.competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': self.team.id,
                'mentor': self.mentor.id,
                }

        response = self.client.post(url, data)

        self.response_403(response)

    def test_remove_mentor_from_team_if_not_teamleader(self):
        self.team_membership.is_leader = False
        self.team_membership.save()

        self.client.force_authenticate(user=self.competitor)

        mentorship = factories.TeamMentorshipFactory(
            team=self.team,
            mentor=self.mentor)

        url = reverse('hack_fmi:team_mentorship', kwargs={'pk': mentorship.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_remove_mentor_from_team(self):

        self.client.force_authenticate(user=self.competitor)

        mentorship = factories.TeamMentorshipFactory(
            team=self.team,
            mentor=self.mentor)

        url = reverse('hack_fmi:team_mentorship', kwargs={'pk': mentorship.id})

        self.assertEqual(TeamMentorship.objects.filter(team=self.team).count(), 1)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMentorship.objects.filter(team=self.team).count(), 0)

    def test_assign_mentor_to_team(self):
        self.team.season.mentor_pick_start_date = date_decrease(10)
        self.team.season.mentor_pick_end_date = date_increase(10)
        self.team.season.save()

        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:team_mentorship')
        data = {
            'team': self.team.id,
            'mentor': self.mentor.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result_mentorship = TeamMentorship.objects.get(team=data['team'])
        self.assertIsNotNone(result_mentorship)
        self.assertIsNotNone(TeamMentorship.objects.get(mentor=data['mentor']))


# @unittest.skip('Skip until further implementation of Hackathon system')
# class RoomTests(APITestCase):

#     def setUp(self):
#         self.season = Season.objects.create(
#             name="HackFMI 1",
#             topic='TestTopic',
#             is_active=True,
#             sign_up_deadline=date_increase(10),
#             mentor_pick_start_date=date_increase(15),
#             mentor_pick_end_date=date_increase(25),
#             make_team_dead_line=date_increase(20),
#         )
#         for i in range(10):
#             Team.objects.create(
#                 name='Pandas{0}'.format(i),
#                 idea_description='GameDevelopers',
#                 repository='https://github.com/HackSoftware',
#                 season=self.season,
#             )
#         for i in [1, 4, 10]:
#             Room.objects.create(
#                 number=100+i,
#                 season=self.season,
#                 capacity=i,
#             )

#     def test_fill_rooms(self):
#         call_command('fillrooms')
#         for team in Team.objects.all():
#             self.assertTrue(team.room.number)

#     def test_more_teams_than_rooms(self):
#         for i in range(10):
#             Team.objects.create(
#                 name='Pandas{0}'.format(i+15),
#                 idea_description='GameDevelopers',
#                 repository='https://github.com/HackSoftware',
#                 season=self.season,
#             )
#         with self.assertRaises(CommandError):
#             call_command('fillrooms')
