from django.shortcuts import render
from .models import chatRoom,Message
from django.contrib.auth.decorators import login_required
from core.models import UserProfile
from landing import models
from random import shuffle
import string
from django.shortcuts import redirect
# Create your views here.


@login_required(login_url="login")
def rooms(request):
	rooms=chatRoom.objects.all()
	context={}
	user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=user.notifications.unread()
	context['notifications_count']=user.notifications.unread().count()
	context['rooms']=rooms

	return render(request,'main/chat/rooms.html',context)

@login_required(login_url="login")
def room(request,slug):
	room=chatRoom.objects.get(slug=slug)
	messages=Message.objects.filter(room=room)
	context={}
	user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=user.notifications.unread()
	context['notifications_count']=user.notifications.unread().count()
	context['room']=room
	context['messages']=messages
	
	return render(request,'main/chat/main.html',context)


def makeName():
	s=string.ascii_letters+string.digits
	a=[x for x in s]
	shuffle(a)
	newString=""
	for i in a:
		newString+=i

	return newString[:16]


@login_required(login_url="login")
def findRoom(request):
	rooms=chatRoom.objects.filter(users=1)
	rooms2=chatRoom.objects.filter(users=0)
	context={}
	user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=user.notifications.unread()
	context['notifications_count']=user.notifications.unread().count()

	# Connecting users to chatrooms with available users
	if rooms.exists():
		firstRoom=rooms.first()
		return redirect("/chat/"+firstRoom.slug)

	# If there's an empty chatroom, connect to that
	elif rooms2.exists():
		secondRoom=rooms2.first()
		profile=UserProfile.objects.get(user=user)
		secondRoom.gender=profile.gender
		return redirect("/chat/"+secondRoom.slug)

	# If there are no rooms, create a new one
	else:
		profile=UserProfile.objects.get(user=user)
		roomName=makeName()
		slug=makeName()
		newRoom=chatRoom.objects.create(name=roomName,slug=slug,gender=profile.gender)
		return redirect("/chat/"+slug)










