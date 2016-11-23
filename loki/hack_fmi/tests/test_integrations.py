from test_plus.test import TestCase

from rest_framework.test import APIClient
from loki.hack_fmi.models import Invitation, TeamMembership
from django.core import mail
from loki.seed import factories
from faker import Factory

faker = Factory.create()


class TestInvitationViewSetIntegration(TestCase):

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

        self.invited_user = factories.CompetitorFactory(email=faker.email())

    def test_whole_flow_of_invitation(self):
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + self.token)
        """
        Competitors(not team leaders) can see the intivations they are dedicated to.
        If competitor is team leader, he can see the members in his team and has options for inviting.
        """
        get_url = self.reverse('hack_fmi:invitation-list')
        response = self.client.get(get_url)
        self.response_200(response)

        """
        TeamLeader can send invitations to other competitors(not base users).
        """
        factories.TeamMembershipFactory(team=self.team,
                                        competitor=self.recipient,
                                        is_leader=True)
        self.assertEquals(Invitation.objects.count(), 0)
        send_invitation_url = self.reverse('hack_fmi:invitation-list')
        data = {'competitor_email': self.invited_user.email}
        response = self.client.post(send_invitation_url, data)
        self.response_201(response)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        """
        Decline invitation if competitor.
        Team Leader cant decline invitations.
        """
        self.invited_user.is_active = True
        self.invited_user.set_password(factories.BaseUserFactory.password)
        self.invited_user.save()
        data = {'email': self.invited_user.email, 'password': factories.BaseUserFactory.password}
        response = self.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=' JWT ' + token)

        invitation = Invitation.objects.filter(competitor=self.invited_user,
                                               team=self.team).first()

        decline_url = self.reverse('hack_fmi:invitation-detail', pk=invitation.id)
        response = self.client.delete(decline_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Invitation.objects.filter(competitor=self.invited_user,
                                                   team=self.team).exists())
        self.assertFalse(TeamMembership.objects.filter(team=self.team,
                                                       competitor=self.invited_user).exists())

        """
        Competitor accepts invitation.
        After the competitor has received an email with notification that he has been requested an invitation,
        he must go to /api/invitation/(?P<pk>[0-9]+)/accept and accept the invitations he has been dedicated to.
        """
        # Factory as we the samo user declined the real invitation upwards.
        fake_invitaion = factories.InvitationFactory(competitor=self.invited_user,
                                                     team=self.team)
        accept_url = self.reverse('hack_fmi:invitation-accept', pk=fake_invitaion.id)
        response = self.client.post(accept_url)
        self.response_200(response)
        self.assertFalse(Invitation.objects.filter(competitor=self.invited_user,
                                                   team=self.team).exists())
        self.assertTrue(TeamMembership.objects.filter(team=self.team,
                                                      competitor=self.invited_user).exists())
