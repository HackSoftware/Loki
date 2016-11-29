from channels import Group
from channels.generic import BaseConsumer


class InvitationServer(BaseConsumer):

    method_mapping = {
        "websocket.connect": "ws_connect",
        "websocket.disconnect": "ws_disconnect",
    }

    def ws_connect(self, message, **kwargs):
        import ipdb; ipdb.set_trace()  # breakpoint 58fcd370 //

        Group("invitations").add(message.reply_channel)

    def ws_disconnect(self, message, **kwargs):
        Group("invitations").discard(message.reply_channel)
