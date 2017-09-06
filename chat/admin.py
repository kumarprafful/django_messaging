from django.contrib import admin
from .models import Room, Message
# Register your models here.

admin.site.register(Room, list_display=["id","title","staff_only"],
							list_display_links=["id","title"],
	)

admin.site.register(Message)