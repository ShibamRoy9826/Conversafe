from django.shortcuts import render
from django.http import HttpResponse
from .models import Message,AIRoom
from django.contrib.auth.decorators import login_required
from core.models import UserProfile
from landing import models
from random import shuffle
import string
from django.shortcuts import redirect
from notification.utilities import allNotifications,notify
# Create your views here.

def makeName():
	s=string.ascii_letters+string.digits
	a=[x for x in s]
	shuffle(a)
	newString=""
	for i in a:
		newString+=i

	return newString[:16]


@login_required(login_url="login")
def AIConnect(request,slug):
	room=AIRoom.objects.get(slug=slug)
	messages=Message.objects.filter(room=room)
	context={}
	user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	context['room']=room
	context['messages']=messages
	return render(request,'main/chat/mainAI.html',context)


@login_required(login_url="login")
def chatWithAI(request):
	# TO REMOVE LATER
	allRooms=AIRoom.objects.all().delete()

	slug=makeName()
	room=AIRoom.objects.create(slug=slug)
	return redirect('/chatWithAI/'+slug)




