###  Libraries and stuff ############################################################
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Some model objects
from .models import chatRoom,Message
from core.models import UserProfile
from landing import models
# For random roomname generation
from random import shuffle
import string
from notification.utils import * # For notifications
################################################################################

#### A Function only for debugging, lists all currently running chat rooms #############
@login_required(login_url="login")
def rooms(request):
    rooms=chatRoom.objects.all()
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['rooms']=rooms

    user = models.AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language

    return render(request,'main/chat/rooms.html',context)

# Connect to a particular chat room 
@login_required(login_url="login")
def room(request,slug):
    room=chatRoom.objects.get(slug=slug)
    messages=Message.objects.filter(room=room)
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['room']=room
    context['messages']=messages
    user = models.AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language


    if room.users >2:
        return HttpResponse("The room you tried to join is Full:( \n Please try joining another room...")
    
    return render(request,'main/chat/main.html',context)

# Generate chat room name
def makeName():
    s=string.ascii_letters+string.digits
    a=[x for x in s]
    shuffle(a)
    newString=""
    for i in a:
        newString+=i

    return newString[:16]

# Find a chat room for the user
@login_required(login_url="login")
def findRoom(request):
    rooms=chatRoom.objects.filter(users=1)
    rooms2=chatRoom.objects.filter(users=0)
    context={}
    user = models.AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language


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


# Create a Private room
@login_required(login_url="login")
def createPrivateRoom(request):
    user = models.AUser.objects.get(pk=request.user.pk)
    roomName=makeName()
    slug=makeName()
    profile=UserProfile.objects.get(user=user)
    r=chatRoom.objects.create(name=roomName,slug=slug,gender=profile.gender)
    return redirect("/chat/private/"+slug)

# Private rooms creation or joining
@login_required(login_url="login")
def privateRoomCreator(request):
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user = models.AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    
    return render(request,'main/chat/createOrJoin.html',context)


# Private Rooms view 
@login_required(login_url="login")
def roomJoinPrivate(request,slug):
    room=chatRoom.objects.get(slug=slug)
    messages=Message.objects.filter(room=room)
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['room']=room
    context['messages']=messages
    user = models.AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language


    if room.users >2:
        return HttpResponse("The room you tried to join is Full:( \n Please try joining another room...")
    
    return render(request,'main/chat/mainPrivate.html',context)
