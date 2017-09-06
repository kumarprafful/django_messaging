from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import index, register

app_name = 'chat'

urlpatterns = [
	url(r'^$', index, name='homepage'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/register/$', register, name='register'),

]