from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Room(models.Model):
	title = models.CharField(max_length=255)

	staff_only = models.BooleanField(default=False)

	@property
	def websocket_group(self):
		'''
		returns the channels group that sockets should
		subscribe to get sent messages as they are generated
		'''
		return Group("room-%s" %self.id)





	def str(self):
		return self.title