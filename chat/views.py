from django.shortcuts import render
from django.http import HttpResponse
from .models import chatRoom,Message
from django.contrib.auth.decorators import login_required
from core.models import UserProfile
from landing import models
from random import shuffle
import string
from notification.utilities import allNotifications, notify
from django.shortcuts import redirect
# Create your views here.


@login_required(login_url="login")
def rooms(request):
	rooms=chatRoom.objects.all()
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	context['rooms']=rooms

	return render(request,'main/chat/rooms.html',context)

@login_required(login_url="login")
def room(request,slug):
	room=chatRoom.objects.get(slug=slug)
	messages=Message.objects.filter(room=room)
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	context['room']=room
	context['messages']=messages


	if room.users >2:
		return HttpResponse("The room you tried to join is Full:( \n Please try joining another room...")
	
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
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()


	# Connecting users to chatrooms with available users
	if rooms.exists():
		firstRoom=rooms.first()
		return redirect("/chat/"+firstRoom.slug)

	# If there's an empty chatroom, delete that , and connect to a new one
	elif rooms2.exists():
		rooms2.delete()

		profile=UserProfile.objects.get(user=user)
		roomName=makeName()
		slug=makeName()
		secondRoom=chatRoom.objects.create(name=roomName,slug=slug,gender=profile.gender)
				
		secondRoom.gender=profile.gender
		return redirect("/chat/"+secondRoom.slug)

	# If there are no rooms, create a new one
	else:
		profile=UserProfile.objects.get(user=user)
		roomName=makeName()
		slug=makeName()
		newRoom=chatRoom.objects.create(name=roomName,slug=slug,gender=profile.gender)
		return redirect("/chat/"+slug)



@login_required(login_url="login")
def createPrivateRoom(request):
	user = models.AUser.objects.get(pk=request.user.pk)
	roomName=makeName()
	slug=makeName()
	profile=UserProfile.objects.get(user=user)
	r=chatRoom.objects.create(name=roomName,slug=slug,gender=profile.gender)
	return redirect("/chat/private/"+slug)

@login_required(login_url="login")
def privateRoomCreator(request):
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	
	return render(request,'main/chat/createOrJoin.html',context)
	
@login_required(login_url="login")
def roomJoinPrivate(request,slug):
	room=chatRoom.objects.get(slug=slug)
	messages=Message.objects.filter(room=room)
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	context['room']=room
	context['messages']=messages


	if room.users >2:
		return HttpResponse("The room you tried to join is Full:( \n Please try joining another room...")
	
	return render(request,'main/chat/mainPrivate.html',context)