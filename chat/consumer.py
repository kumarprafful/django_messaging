from channels.auth import channel_session_user_from_http

@channel_session_user_from_http
def ws_connect(message):
	message.reply_channel.send({"accept": True})
	message.channel_session['rooms'] = []

@channel_session_user
def ws_disconnect(message):
	#unsubscribe from any connected rooms
	for room_id in message.channel_session.get("rooms", set()):
		try:
			room = Room.objects.get(pk=room_id)
			#removes users from the rooms's send group. if this doesn't get run,
			#user will be removed once his first reply message expires.
			room.websocket_group.discard(message.reply_channel)
		except Room.DoesNotExist:
			pass