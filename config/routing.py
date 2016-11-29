from channels.routing import route_class
from loki.hack_fmi import consumers


channel_routing = [
    # ws://localhost:8000/invitations
    route_class(consumers.InvitationServer, path=r'^/invitations')
]
