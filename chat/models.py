import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group
from .settings import MSG_TYPE_MESSAGE
# Create your models here.

@python_2_unicode_compatible
class Room(models.Model):
	title = models.CharField(max_length=255)

	staff_only = models.BooleanField(default=False)

	def __str__(self):
		return self.title



	@property
	def websocket_group(self):
		'''
		returns the channels group that sockets should
		subscribe to get sent messages as they are generated
		'''
		return Group("room-%s" %self.id)

	def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
		"""
		called to send a message to the room on behalf of a user.
		"""
		final_msg = {'room': str(self.id), 'message':message, 'username': user.username, 'msg_type': msg_type}

		#send out the message to everyone in the room
		self.websocket_group.send(
			{"text": json.dumps(final_msg)}
		)
		if(message):
			msg = Message()
			msg.room = Room.objects.get(pk=self.id)
			msg.username = user.username
			msg.message = message
			msg.save()




class Message(models.Model):
	room = models.ForeignKey(Room)
	username = models.CharField(max_length=255)
	message = models.TextField(max_length=1024)

	def __str__(self):
		return self.room.title + self.username
