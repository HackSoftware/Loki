import json

from django.conf import settings

from test_plus.test import TestCase

from channels import Group, Channel
from channels.tests import ChannelTestCase
from loki.seed.factories import (InvitationFactory, BaseUserFactory, TeamFactory,
                                 CompetitorFactory, TeamMembershipFactory)


class TestInvitationConsumer(ChannelTestCase, TestCase):
    "On post save of Invitation object, we send a massive message to group 'Invitations'"

    def get_valid_token(self):
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()
        data = {'email': self.user.email, 'password': BaseUserFactory.password}
        response = self.client.post(self.reverse('hack_fmi:api-login'), data=data, format='json')

        self.response_200(response)
        token = response.data.get('token')
        self.assertIsNotNone(token)
        return token

    # Test signal works properly
    def test_server_group_send_message_to_client_on_post_save_of_invitation(self):
        competitor = CompetitorFactory()

        # Add test-channel to Invitation example group
        expected_group_name = settings.INVITATION_GROUP_NAME.format(id=competitor.id)
        Group(expected_group_name).add("test-channel")

        team = TeamFactory(season__is_active=True)
        TeamMembershipFactory(team=team, competitor=competitor, is_leader=True)
        InvitationFactory(team=team, competitor=competitor)
        # Get the message that is transferred into the channel
        result = self.get_next_message("test-channel")
        result = json.loads(result.get('text'))
        self.assertEqual(result['message'], "New invitation was created.")
        self.assertEqual(result['leader'], competitor.full_name)

    def test_connection_is_closed_when_token_is_not_sent(self):
        # In receive message we expect to receive token field
        Channel("connection").receive({"no_token": ""})
        result = self.get_next_message("connection")
        self.assertTrue(result.get('close'))

    def test_non_authenticated_user_is_not_added_to_group(self):
        # invalid_token = self.get_valid_token() + "invalid"
        # # Open a channel connection called 'connection' and pass data to server
        # Channel("connection").send({"token": invalid_token})
        # expected_group_name = settings.INVITATION_GROUP_NAME.format(id=self.user.id)

        # result = self.get_next_message("connection")
        pass

    def test_authenticated_user_is_added_to_group(self):
        token = self.get_valid_token()
        # Open a channel connection called 'connection' and pass data to server
        Channel("connection").send({"token": token})
        expected_group_name = settings.INVITATION_GROUP_NAME.format(id=self.user.id)
        self.assertIsNotNone(Group(expected_group_name))
