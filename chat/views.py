from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from .forms import UserForm
# Create your views here.


def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
	return render(request, 'registration/user_register.html', {'registered': registered, 'user_form': user_form})


@login_required
def index(request):
	rooms = Room.objects.order_by("title")
	return render(request, "chat/index.html",{"rooms":rooms,})