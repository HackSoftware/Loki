import time
from django.core import mail
from rest_framework.test import APIClient

from test_plus.test import TestCase

from loki.hack_fmi.models import Invitation, TeamMembership, BlackListToken
from loki.seed import factories
from loki.seed.factories import (BaseUserFactory,)

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
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
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
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

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


class TestJWTIntegration(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()

    def login(self):

        data = {'email': self.user.email, 'password': BaseUserFactory.password}
        response = self.client.post(self.reverse('hack_fmi:api-login'), data=data, format='json')
        self.response_200(response)
        token = response.data.get('token')
        self.assertIsNotNone(token)
        return token

    def authenticate(self):
        existing_token = self.login()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + existing_token)
        return existing_token

    def refresh_token(self, existing_token):
        data = {'token': existing_token}
        """
        The jwt hashing depends on timestamp at the exact moment.
        Otherwise, it generates same tokens.
        """
        time.sleep(1)
        response = self.client.post(self.reverse('hack_fmi:api-refresh'), data=data)
        self.response_200(response)
        new_token = response.data.get('token')
        self.assertNotEqual(new_token, existing_token)
        return {'existing_token': existing_token,
                'new_token': new_token}

    def logout(self):
        url = self.reverse('hack_fmi:api-logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 202)
        return response

    def test_cant_access_api_with_already_refreshed_token(self):
        existing_token = self.authenticate()
        """
        The token has just been refreshed, but it is still active, until it expires
        """
        tokens = self.refresh_token(existing_token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + tokens['existing_token'])
        response = self.client.get(self.reverse('hack_fmi:me'))
        self.response_403(response)

    def test_can_access_api_with_new_token_after_refresh(self):
        existing_token = self.authenticate()
        tokens = self.refresh_token(existing_token)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + tokens['new_token'])
        response = self.client.get(self.reverse('hack_fmi:me'))
        self.response_200(response)

    def test_cant_access_api_with_blacklisted_token_after_logout(self):
        existing_token = self.login()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + existing_token)

        self.logout()

        self.assertTrue(BlackListToken.objects.filter(token='JWT ' + existing_token).exists())

        # Authenticate with the same blacklisted token
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + existing_token)

        response = self.client.get(self.reverse('hack_fmi:me'))
        self.response_403(response)

    def test_refresh_immediately_after_login_does_not_blacklist_the_login_token(self):
        """
        The refresh token will be the same as login token if we refresh immediately after login.
        Thats why in the CustomRefreshJSONWebTokenAPIView we check whether the newly refresh token is the same
        as the previous token.
        """
        existing_token = self.authenticate()
        data = {'token': existing_token}

        response = self.client.post(self.reverse('hack_fmi:api-refresh'), data=data)
        self.response_200(response)
        new_token = response.data.get('token')

        self.assertEqual(new_token, existing_token)
        self.assertFalse(BlackListToken.objects.filter(token=existing_token).exists())

    def test_can_access_apis_with_login_token_after_immediate_refresh_after_login(self):
        """
        After immediate refresh after login, the login token must not be blacklisted
        as it is the same as the newly refreshed one.We must be able to access apis
        with the login token.
        """
        existing_token = self.authenticate()
        data = {'token': existing_token}

        response = self.client.post(self.reverse('hack_fmi:api-refresh'), data=data)
        self.response_200(response)

        new_token = response.data.get('token')
        self.assertEqual(new_token, existing_token)
        self.assertFalse(BlackListToken.objects.filter(token=existing_token).exists())

        response = self.client.get(self.reverse('hack_fmi:me'))

        self.response_200(response)
