from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FriendRequest,FriendList
from landing.models import AUser
from notification.utilities import notify,allNotifications
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect

# Create your views here.

@login_required(login_url="login")
def friends(request):
	context={}
	context['friendRequests']=FriendRequest.objects.filter(receiver=request.user)
	context['friends']=FriendList.objects.get(user=request.user).friends.all()
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/friends.html",context)

def searchPeople(request):
	if request.method == 'POST':
		context={}
		context['notifications_unread']=allNotifications(request.user.pk)
		context['notifications_count']=allNotifications(request.user.pk).count()
		query = request.POST.get('searchQuery')
		context['results']=AUser.objects.filter(username__icontains=query)[:10]
		return render(request,"main/func/showResults.html",context)
	return redirect("/")
		

def sendFriendRequest(request):
	if request.method == 'POST':
		userToAddUsername = request.POST.get('userToAdd')
		try:
			# deleteNotification(request.user,userToAdd)
			userToAdd=AUser.objects.get(username=userToAddUsername)

			# If A request has already been sent
			if FriendRequest.objects.filter(sender=request.user, receiver=userToAdd):
				return HttpResponse("Friend Request already sent...")

			# If the given user is already a friend of the user
			elif FriendList.objects.get(user=request.user).isFriend(userToAdd):
				return HttpResponse("Already friend")
			else:
				friendReq=FriendRequest.objects.create(sender=request.user, receiver=userToAdd)
				notify(userToAdd, "You have a friend request", f"{userToAdd.username} wants to be your friend")
				return HttpResponse("Success")
		except Exception as E:
			print("Some Serious issue occured")
			print(E)
			return HttpResponse("User not found")
	else:
		# pass
		return HttpResponse("Not allowed", status=405)

def unFriend(request):
	if request.method == 'POST':
		userToUnfriendUsername = request.POST.get('userToUnFriend')
		try:
			# deleteNotification(request.user,userToAdd)
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
		# pass
		return HttpResponse("Not allowed", status=405)

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
		# pass
		return HttpResponse("Not allowed", status=405)

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
		# pass
		return HttpResponse("Not allowed", status=405)
