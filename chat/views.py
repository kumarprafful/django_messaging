from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
# Create your views here.

@login_required
def index(request):
	rooms = Room.objects.order_by("title")
	return render(request, "chat/index.html",{"rooms":rooms,})