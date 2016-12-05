import json
import time
from datetime import timedelta

from django.conf import settings

from test_plus.test import TestCase
from channels import Group, Channel
from channels.tests import ChannelTestCase

from loki.seed.factories import (InvitationFactory, BaseUserFactory, TeamFactory,
                                 CompetitorFactory, TeamMembershipFactory)
from loki.hack_fmi.consumers import InvitationConsumer

from faker import Factory

faker = Factory.create()


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

    def test_connection_is_closed_when_token_is_empty_string(self):
        # In receive message we expect to receive token field
        channel_name = u"websocket.receive"

        text = {"token": ""}

        Channel(channel_name).send({'path': '/', 'text': json.dumps(text), "reply_channel": "angular_client"})
        message = self.get_next_message(channel_name, require=True)
        InvitationConsumer(message)

        result = self.get_next_message(message.reply_channel.name, require=True)
        self.assertTrue(result.get('close'))

    def test_non_authenticated_user_is_not_added_to_group(self):
        channel_name = u"websocket.receive"

        invalid_token = self.get_valid_token() + "invalid"
        text = {"token": invalid_token}

        Channel(channel_name).send({'path': '/', 'text': json.dumps(text), "reply_channel": "angular_client"})
        message = self.get_next_message(channel_name, require=True)
        InvitationConsumer(message)

        result = self.get_next_message(message.reply_channel.name, require=True)

        self.assertTrue(result.get('close'))

    def test_authenticated_user_is_added_to_group(self):
        token = self.get_valid_token()
        # Channel name maps the method that is expected to be run -> InvitationConsumer.method_mapping
        channel_name = u"websocket.receive"
        text = {"token": token}

        # Open a channel connection called 'connection' and pass data to server from reply_channel
        # reply_channel is the other hand of the connection /angular client/
        Channel(channel_name).send({'path': '/', 'text': json.dumps(text), "reply_channel": "angular_client"})

        message = self.get_next_message(channel_name, require=True)
        InvitationConsumer(message)

        result = self.get_next_message(message.reply_channel.name, require=True)

        self.assertEquals(result.get("text"), InvitationConsumer.USER_ADDED_TO_GROUP_MESSAGE)

    def test_authentication_failed_if_there_is_no_token_key_in_sended_messsage(self):
        channel_name = u"websocket.receive"
        text = {"non_token_field": faker.word()}

        Channel(channel_name).send({'path': '/', 'text': json.dumps(text), "reply_channel": "angular_client"})

        message = self.get_next_message(channel_name, require=True)
        InvitationConsumer(message)

        result = self.get_next_message(message.reply_channel.name, require=True)

        self.assertTrue(result.get('close'))

    def test_connection_closed_when_signiture_has_expired(self):
        settings.JWT_AUTH['JWT_EXPIRATION_DELTA'] = timedelta(seconds=60)

        token = self.get_valid_token()
        time.sleep(60)

        channel_name = u"websocket.receive"
        text = {"token": token}

        Channel(channel_name).send({'text': json.dumps(text), "reply_channel": "angular_client"})

        message = self.get_next_message(channel_name, require=True)
        InvitationConsumer(message)

        result = self.get_next_message(message.reply_channel.name, require=True)

        self.assertTrue(result.get('close'))

    def test_connection_closed_when_user_with_decoded_id_from_token_does_not_exist(self):
        pass

