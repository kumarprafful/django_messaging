from functools import wraps
from .exceptions import ClientError
from .models import Room

def catch_client_error(func):
	"""
	decorator to catch the clienterror exception and translate it into a reply
	"""
	@wraps(func)
	def inner(message, args, **kwargs):
		try:
			return func(message, args, **kwargs)
		except ClientError as e:
			#if we catch a client error, tell it to send an error to send it
			#to send it back to the client on their reply_channel
			e.send_to(message.reply_channel)
		return inner

def get_room_or_error(room_id, user):
	"""
	tries to fetch a room for the user, checkingthe permission along
	the way
	"""
	#chk if the user is logged in
	if not user.is_authenticated():
		raise ClientError("USER_HAS_TO_lOGIN")
		#find the room they requested(by id)
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExists:
			raise ClientError("ROOM_INVALID")
		#chking permissions
		if room.staff_only and not user.is_staff:
			raise ClientError("ROOM_ACCESS_DENIED")
		return room
	