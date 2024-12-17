############ Libraries and stuff ################################################
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Some Model objects
from .models import Message,AIRoom
from core.models import UserProfile
from landing import models
from random import shuffle # for making random room name
import string # Content to generate random room name
from notification.utils import notifs, notifCount # For notifications
###################################################################################

# Generates random room name
def makeName():
    s=string.ascii_letters+string.digits
    a=[x for x in s]
    shuffle(a)
    newString=""
    for i in a:
        newString+=i

    return newString[:16]


# AI Chat page
@login_required(login_url="login")
def AIConnect(request,slug):
    room=AIRoom.objects.get(slug=slug)
    messages=Message.objects.filter(room=room)
    context={}
    user = models.AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['room']=room
    context['messages']=messages
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    return render(request,'main/chat/mainAI.html',context)

# Connecting to a particular room
@login_required(login_url="login")
def chatWithAI(request):
    # Temporary workaround
    allRooms=AIRoom.objects.all().delete()

    slug=makeName()
    room=AIRoom.objects.create(slug=slug)
    return redirect('/chatWithAI/'+slug)

