import unittest
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.management.base import CommandError

from post_office import mail

from rest_framework import status
from rest_framework.test import APIClient
from test_plus.test import TestCase
from post_office.models import EmailTemplate

from ..helper import date_increase, date_decrease
from ..models import (TeamMembership,
                      Season, Team, Invitation, Room,
                      TeamMentorship, Mentor)

from seed import factories

from faker import Factory

faker = Factory.create()


class SkillTests(TestCase):

    def test_get_skill(self):
        skill = factories.SkillFactory()
        url = reverse('hack_fmi:skills')
        response = self.client.get(url)

        self.response_200(response)
        self.assertEqual(response.data.pop()['name'], skill.name)


class MentorListAPIViewTest(TestCase):

    def test_get_all_mentors_for_current_active_season(self):
        self.client = APIClient()

        company = factories.HackFmiPartnerFactory()

        non_active_season = factories.SeasonFactory(
            is_active=False)

        active_season = factories.SeasonFactory(
            is_active=True)

        self.assertEqual(Mentor.objects.all().count(), 0)

        mentor = factories.MentorFactory(
            from_company=company
        )
        mentor2 = factories.MentorFactory(
            from_company=company
        )
        active_season.mentor_set.add(mentor)
        active_season.mentor_set.add(mentor2)
        active_season.save()

        mentor3 = factories.MentorFactory(
            from_company=company
        )
        non_active_season.mentor_set.add(mentor3)
        non_active_season.save()

        student = factories.StudentFactory(
            email=faker.email()
        )
        self.client.force_authenticate(student)
        url = reverse('hack_fmi:mentors')

        response = self.client.get(url)
        current_season = Season.objects.filter(is_active=True).first()
        mentors_for_current_season = current_season.mentor_set.count()

        self.response_200(response)
        self.assertEqual(len(response.data), mentors_for_current_season)


class SeasonViewTest(TestCase):

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

        self.response_200(response)

        self.assertEqual(response.data['name'], self.active_season.name)
        self.assertTrue(Season.objects.filter(is_active=True).exists())

    def test_season_deactivates_automatically(self):
        new_active_season = factories.SeasonFactory(
            is_active=True,
        )

        self.assertTrue(Season.objects.filter(is_active=True).exists())
        self.assertFalse(Season.objects.get(name=self.active_season.name).is_active)
        self.assertTrue(Season.objects.get(name=new_active_season.name).is_active)


class PublicTeamViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_teams_for_current_season(self):
        active_season = factories.SeasonFactory(
            is_active=True
        )
        room = factories.RoomFactory(season=active_season)
        team = factories.TeamFactory(
            season=active_season,
            room=room
        )
        url = reverse('hack_fmi:public_teams')

        teams_in_active_season = Team.objects.filter(season__is_active=True).count()

        response = self.client.get(url)

        self.response_200(response)
        self.assertEqual(len(response.data), teams_in_active_season)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], team.name)

    def test_get_teams_only_from_current_active_season(self):
        active_season = factories.SeasonFactory(
            is_active=True
        )
        room = factories.RoomFactory(season=active_season)
        team_in_active_season = factories.TeamFactory(
            name=faker.name(),
            season=active_season,
            room=room,
        )
        non_active_season = factories.SeasonFactory(
            is_active=False
        )
        room_for_non_active_season = factories.RoomFactory(season=non_active_season)
        team_in_non_active_season = factories.TeamFactory(
            name=faker.name(),
            season=non_active_season,
            room=room_for_non_active_season,
        )
        url = reverse('hack_fmi:public_teams')

        teams_in_active_season = Team.objects.filter(season__is_active=True).count()

        response = self.client.get(url)

        self.response_200(response)
        self.assertEqual(len(response.data), teams_in_active_season)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], team_in_active_season.name)
        self.assertNotEqual(response.data[0]['name'], team_in_non_active_season.name)


class TeamAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.active_season = factories.SeasonFactory(
            is_active=True,
        )
        self.room = factories.RoomFactory(season=self.active_season)

    def test_non_hackfmi_user_cant_get_to_team(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        url = reverse('hack_fmi:teams')

        response = self.client.get(url, kwargs={'pk': faker.random_number(digits=1)})

        self.response_401(response)

    def test_competitor_can_get_team_information_for_his_team_in_active_season_within_the_season_deadlines(self):
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=False,
        )
        self.client.force_authenticate(competitor)

        url = reverse('hack_fmi:teams')

        response = self.client.get(url, kwargs={'pk': team.id})

        self.response_200(response)

    def test_non_teamleaders_cant_change_team(self):
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=False,
        )
        self.client.force_authenticate(competitor)

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_only_leader_can_change_team(self):
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(competitor)

        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.patch(url, data)

        self.response_200(response)
        self.assertIsNotNone(Team.objects.get(name=data['name']))
        self.assertIsNotNone(Team.objects.get(idea_description=data['idea_description']))

    def test_user_can_get_to_teams_in_non_active_seasons(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        non_active_season = factories.SeasonFactory(
            is_active=False
        )
        team = factories.TeamFactory(
            season=non_active_season,
            room=self.room)
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=False,
        )
        self.client.force_authenticate(competitor)
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.get(url)

        self.response_200(response)

    def test_user_cannot_change_teams_in_non_active_seasons(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        non_active_season = factories.SeasonFactory(
            is_active=False
        )
        team = factories.TeamFactory(
            season=non_active_season,
            room=self.room
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=False,
        )
        self.client.force_authenticate(competitor)
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_leader_cannot_change_teams_in_non_active_seasons(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        non_active_season = factories.SeasonFactory(
            is_active=False
        )
        team = factories.TeamFactory(
            season=non_active_season,
            room=self.room
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(competitor)
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_get_team_within_current_season_deadlines(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        self.client.force_authenticate(competitor)
        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.get(url)

        self.response_200(response)

    def test_cannot_change_team_out_of_the_current_season_deadline(self):
        self.active_season.make_team_dead_line = date_increase(100)
        self.active_season.save()

        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.active_season,
            room=self.room
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        data = {
            'name': faker.name(),
            'idea_description': faker.paragraph(),
        }

        self.client.force_authenticate(competitor)

        url = reverse('hack_fmi:teams', kwargs={'pk': team.id})

        response = self.client.patch(url, data)

        self.response_403(response)

    def test_whether_when_you_register_your_own_team_you_become_leader_of_that_team(self):
        skill = factories.SkillFactory()
        competitor = factories.CompetitorFactory(
            email=faker.email(),
        )

        team_data = {
            'name': faker.name(),
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],

        }

        self.assertFalse(Team.objects.filter(name=team_data['name']).exists())
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:teams')
        response = self.client.post(url, team_data)

        self.response_201(response)
        self.assertTrue(Team.objects.filter(name=team_data['name']).exists())
        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(len(response.data['technologies']), 1)
        self.assertTrue(TeamMembership.objects.filter(competitor=competitor, is_leader=True).exists())
        self.assertEqual(TeamMentorship.objects.all().count(), 0)

    def test_cant_register_team_that_has_the_same_name(self):
        skill = factories.SkillFactory()
        competitor = factories.CompetitorFactory(
            email=faker.email(),
        )

        team_data = {
            'name': faker.name(),
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],

        }
        registered_team = factories.TeamFactory(**team_data)

        self.assertTrue(Team.objects.filter(name=team_data['name']).exists())

        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:teams')
        response = self.client.post(url, team_data)

        self.response_403(response)

    def test_cant_register_other_team_if_you_are_a_leader_of_already_existing_team(self):
        skill = factories.SkillFactory()
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        existing_team = factories.TeamFactory()
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=existing_team,
            is_leader=True
        )

        self.client.force_authenticate(competitor)

        team_data = {
            'name': faker.name(),
            'idea_description': faker.text(),
            'repository': faker.url(),
            'technologies': [skill.id, ],

        }
        self.assertFalse(Team.objects.filter(name=team_data['name']).exists())

        url = reverse('hack_fmi:teams')
        response = self.client.post(url, team_data)

        self.response_403(response)
        self.assertFalse(Team.objects.filter(name=team_data['name']).exists())


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

    def test_user_cant_leave_team_if_he_has_not_been_a_member_in_that_team(self):
        other_competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        other_membership = factories.TeamMembershipFactory(
            competitor=other_competitor,
            team=self.team,
            is_leader=False,
        )
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

        self.template = EmailTemplate.objects.create(
            name='hackfmi_team_invite',
            subject='Invitation for HackFMI membership',
            content=faker.paragraph(),
        )

        self.season = factories.SeasonFactory(
            is_active=True,
        )

    def test_send_invitation_for_team(self):
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
        self.assertEqual(mail.get_queued().last().message, self.template.content)

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

        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)

        self.response_403(response)

    def test_accept_invitation_that_is_not_yours(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        self.client.force_authenticate(user=competitor)

        other_competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.season
        )
        inv = factories.InvitationFactory(
            team=team,
            competitor=other_competitor
        )

        url = reverse('hack_fmi:invitation-accept', kwargs={'pk': inv.id})

        response = self.client.post(url)

        self.response_403(response)

    def test_decline_invitation_if_you_are_already_a_member_in_other_team(self):
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

        factories.TeamMembershipFactory(
            team=team,
            competitor=competitor,
        )

        invitation = factories.InvitationFactory(
            team=team,
            competitor=competitor
        )
        self.assertEqual(Invitation.objects.all().count(), 1)

        url = reverse('hack_fmi:invitation-detail', kwargs={'pk': invitation.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Invitation.objects.all().count(), 0)

    def test_decline_invitation_that_is_not_yours(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )

        other_competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            season=self.season
        )
        self.client.force_authenticate(user=competitor)

        invitation = factories.InvitationFactory(
            team=team,
            competitor=other_competitor
        )
        self.assertEqual(Invitation.objects.all().count(), 1)
        url = reverse('hack_fmi:invitation-detail', kwargs={'pk': invitation.id})

        response = self.client.delete(url)

        self.response_403(response)
        self.assertFalse(TeamMembership.objects.filter(competitor=invitation.competitor).exists())
        self.assertEqual(Invitation.objects.all().count(), 1)


class TeamMentorshipTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.season = factories.SeasonFactory(
            is_active=True,
        )
        self.competitor = factories.CompetitorFactory(
            email=faker.email(),
        )
        self.company = factories.HackFmiPartnerFactory()

    def test_cannot_assign_mentor_if_you_are_not_hackfmi_user(self):
        competitor = factories.CompetitorFactory(
            email=faker.email(),)
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )
        self.client.force_authenticate(competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': team.id,
                'mentor': mentor.id,
                }

        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_mentor_if_not_leader_team(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
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
        mentor = factories.MentorFactory(
            from_company=self.company,
        )

        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': team.id,
                'mentor': mentor.id,
                }

        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_more_than_allowed_mentors_for_that_season(self):
        self.season.max_mentor_pick = 1
        self.season.save()

        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )
        other_mentor = factories.MentorFactory(
            from_company=self.company,
        )

        factories.TeamMentorshipFactory(
            team=team,
            mentor=mentor
        )
        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': team.id,
                'mentor': other_mentor.id
                }

        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_mentor_before_mentor_pick_has_started(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )

        team.season.mentor_pick_start_date = date_increase(10)
        team.season.mentor_pick_end_date = date_increase(10)
        team.season.save()

        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )

        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': team.id,
                'mentor': mentor.id,
                }
        response = self.client.post(url, data)

        self.response_403(response)

    def test_assign_mentor_after_mentor_pick_has_ended(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )

        team.season.mentor_pick_start_date = date_decrease(10)
        team.season.mentor_pick_end_date = date_decrease(10)
        team.season.save()

        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )

        self.client.force_authenticate(user=competitor)

        url = reverse('hack_fmi:team_mentorship')

        data = {'team': team.id,
                'mentor': mentor.id,
                }
        response = self.client.post(url, data)

        self.response_403(response)

    def test_remove_mentor_from_team_if_not_teamleader(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
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
        mentor = factories.MentorFactory(
            from_company=self.company,
        )
        self.client.force_authenticate(user=competitor)

        mentorship = factories.TeamMentorshipFactory(
            team=team,
            mentor=mentor
        )

        url = reverse('hack_fmi:team_mentorship', kwargs={'pk': mentorship.id})

        response = self.client.delete(url)

        self.response_403(response)

    def test_remove_mentor_from_team_if_leader(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )
        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )
        self.client.force_authenticate(user=competitor)

        mentorship = factories.TeamMentorshipFactory(
            team=team,
            mentor=mentor
        )

        url = reverse('hack_fmi:team_mentorship', kwargs={'pk': mentorship.id})

        self.assertEqual(TeamMentorship.objects.filter(team=team).count(), 1)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TeamMentorship.objects.filter(team=team).count(), 0)

    def test_assign_mentor_to_team_in_mentor_pick_time(self):
        competitor = factories.CompetitorFactory(
            email=faker.email()
        )
        team = factories.TeamFactory(
            name=faker.name(),
            season=self.season,
        )

        team.season.mentor_pick_start_date = date_decrease(10)
        team.season.mentor_pick_end_date = date_increase(10)
        team.season.save()

        factories.TeamMembershipFactory(
            competitor=competitor,
            team=team,
            is_leader=True,
        )
        mentor = factories.MentorFactory(
            from_company=self.company,
        )
        self.client.force_authenticate(user=competitor)
        url = reverse('hack_fmi:team_mentorship')
        data = {
            'team': team.id,
            'mentor': mentor.id,
        }
        response = self.client.post(url, data)

        self.response_201(response)
        self.assertTrue(TeamMentorship.objects.filter(team=data['team']).exists())
        self.assertTrue(TeamMentorship.objects.filter(mentor=data['mentor']).exists())


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
