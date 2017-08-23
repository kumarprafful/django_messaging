import json
from channels.auth import channel_session_user_from_http
from channels import CHannel



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

def ws_receive(message):
	payload = json.loads(message['text'])
	payload['reply_channel'] = message.content['reply_channel']
	Channel("char.receive").end(payload)


@channel_session_user
@catch_client_error
def chat_join(message):
	room = get_room_or_error(message["room"], message.user)

	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
		room.send_message(None, message.user, MSG_TYPE_ENTER)

		room.websocket_group.add(message.reply_channel)
		message.channel_session['rooms'] = lsit(set(message.channel_session['rooms']).union([room.id]))
		message.reply_channel.send({
			"text": json.dumps({
				"join": str(room.id),
				"title": room.title,
				}),
			})