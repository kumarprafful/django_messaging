from channels import route
from .consumers import ws_connect, ws_receive, ws_disconnect, chat_join, chat_leave, chat_send

websocket_routing = [
	#called when websockets connect
	route("websocket.connect", ws_connect),

	#called when websockets get sent a data frame
	route("websocket.receive", ws_receive),

	#called when websockets disconnects
	route("websocket.disconnect", ws_disconnect),

]

custom_routing = [
	#handling different chat commands (websocket.receive is decodedand put onto
	# this channel) -routed on the command attribute of the decoded msg

	route("chat.receive", chat_join, command="^join$"),
	route("chat.receive", chat_leave, command="^leave$"),
	route("chat.receive", chat_send, command="^send$"),	
]