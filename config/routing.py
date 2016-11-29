from channels.routing import route
from loki.hack_fmi.consumers import ws_connect, ws_disconnect


channel_routing = [
    route("websocket.connect", ws_connect, path=r'^'),
    route("websocket.disconnect", ws_disconnect),
]
