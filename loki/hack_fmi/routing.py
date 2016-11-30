from channels.routing import route_class

from .consumers import InvitationConsumer


hackfmi_routing = [
    route_class(InvitationConsumer, path=r'^/invitations')
]
