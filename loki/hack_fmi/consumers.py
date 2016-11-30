from channels.generic.websockets import WebsocketConsumer


class InvitationConsumer(WebsocketConsumer):
    groups = ('Invitation', )

    def connect(self, message, **kwargs):
        print("connect")

    def disconnect(self, message, **kwargs):
        print("disconnect")
