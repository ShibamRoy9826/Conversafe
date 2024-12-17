###  Libraries and stuff ############################################################
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
# Some model objects
from .models import FriendRequest,FriendList
from landing.models import AUser
from core.models import UserProfile
from notification.utils import * # For notifications
################################################################################

# Friends page
@login_required(login_url="login")
def friends(request):
    context={}
    context['friendRequests']=FriendRequest.objects.filter(receiver=request.user)
    context['friends']=FriendList.objects.get(user=request.user).friends.all()
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)

    user = AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    return render(request,"main/func/friends.html",context)


# Search for people
@login_required(login_url="login")
def searchPeople(request):
    if request.method == 'POST':
        context={}
        context['notifications_unread']=['']
        context['notifications_count']=0
        query = request.POST.get('searchQuery')
        # Search for people with same username as query with top 10 results
        context['results']=AUser.objects.filter(username__icontains=query)[:10]

        user = AUser.objects.get(pk=request.user.pk)
        user_profile = UserProfile.objects.get(user=user)
        context["lang"]=user_profile.language
        return render(request,"main/func/showResults.html",context)
    return redirect("/")
        

# Send friend request
@login_required(login_url="login")
def sendFriendRequest(request):
    if request.method == 'POST':
        userToAddUsername = request.POST.get('userToAdd')
        try:
            userToAdd=AUser.objects.get(username=userToAddUsername)

            # If A request has already been sent
            if FriendRequest.objects.filter(sender=request.user, receiver=userToAdd):
                return HttpResponse("Friend Request already sent...")

            # If the given user is already a friend of the user
            elif FriendList.objects.get(user=request.user).isFriend(userToAdd):
                return HttpResponse("Already friend")
            else:
                friendReq=FriendRequest.objects.create(sender=request.user, receiver=userToAdd)
                #Send a notificatoin to let the user know of their friend request
                notify(userToAdd, "You have a friend request", f"{request.user.username} wants to be your friend")
                return HttpResponse("Success")
        except Exception as E:
            print("Some Serious issue occured")
            print(E)
            return HttpResponse("User not found")
    else:
        return HttpResponse("Not allowed", status=405)


# Unfriend someone
@login_required(login_url="login")
def unFriend(request):
    if request.method == 'POST':
        userToUnfriendUsername = request.POST.get('userToUnFriend')
        try:
            userToUnfriend=AUser.objects.get(username=userToUnfriendUsername)
            userFriendList=FriendList.objects.get(user=request.user)

            # Only if that person is already a friend
            if userFriendList.isFriend(userToUnfriend):
                userFriendList.unfriend(userToUnfriend)
            return HttpResponse("Success")
        except Exception as E:
            print("Some Serious issue occured")
            print(E)
            return HttpResponse("User not found")
    else:
        # pass
        return HttpResponse("Not allowed", status=405)

# Cancelling existing friend request
@login_required(login_url="login")
def CancelRequest(request):
    if request.method == 'POST':
        userToCancelReqUsername = request.POST.get('userCancelRequest')
        try:
            userToCancelReq=AUser.objects.get(username=userToCancelReqUsername)

            req=FriendRequest.objects.get(sender=request.user, receiver=userToCancelReq)
            req.cancel()
            return HttpResponse("Success")

        except Exception as E:
            print("Some Serious issue occured")
            print(E)
            return HttpResponse("User not found")
    else:
        return HttpResponse("Not allowed", status=405)


# Accepting Friend request
@login_required(login_url="login")
def AcceptRequest(request):
    if request.method == 'POST':
        userAcceptUsername = request.POST.get('userAccept')
        try:
            userAcceptReq=AUser.objects.get(username=userAcceptUsername)

            req=FriendRequest.objects.get(sender=userAcceptReq, receiver=request.user)
            req.accept()

            return HttpResponse("Success")

        except Exception as E:
            print("Some Serious issue occured")
            print(E)
            return HttpResponse("User not found")
    else:
        return HttpResponse("Not allowed", status=405)

# Declining Friend request
def DeclineRequest(request):
    if request.method == 'POST':
        userDeclineUsername = request.POST.get('userDecline')
        try:
            userDeclineReq=AUser.objects.get(username=userDeclineUsername)

            req=FriendRequest.objects.get(sender=userDeclineReq, receiver=request.user)
            req.decline()
            
            return HttpResponse("Success")

        except Exception as E:
            print("Some Serious issue occured")
            print(E)
            return HttpResponse("User not found")
    else:
        return HttpResponse("Not allowed", status=405)
