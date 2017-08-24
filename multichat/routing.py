from channels import route
from channels import include

def message_handler(message):
	print(message['text'])

channel_routing = [
	route("websocket.receive", message_handler),
	include("chat.routing.websocket_routing", path=r"^/chat/stream"),
	include("chat.routing.custom_routing"),
	
    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.

]


