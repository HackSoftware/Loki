from channels import Group
from channels.tests import ChannelTestCase
from loki.seed.factories import InvitationFactory

# auth


class MyTests(ChannelTestCase):
    "On post save of Invitation object, we send a massive message to group 'Invitations'"

    def test_server_group_send_message_to_client_on_post_save_of_invitation(self):
        # Add test-channel to Invitation group
        Group("Invitation").add("test-channel")

        InvitationFactory()
        # Get the message that is transferred into the channel
        result = self.get_next_message("test-channel")
        self.assertEqual(result.get('text'), "New invitation was created.")

    def test_server_doesnt_send_message_to_client_if_the_group_is_not_called_invitaion(self):
        # Add test-channel to Invitation group
        Group("Fake").add("test-channel")

        InvitationFactory()
        # Get the message that is transferred into the channel
        result = self.get_next_message("test-channel")
        self.assertIsNone(result)

    def test_non_authenticated_user_cant_connect_to_server(self):
        pass

    def test_non_authenticated_user_is_not_added_to_group_Invitations(self):
        pass

    def test_autenticated_user_is_connected_to_group_invitation(self):
        pass

    def test_server_sends_back_message_to_all_authenticated_members_of_group_if_an_ivitation_is_made(self):
        pass
