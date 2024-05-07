from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from landing.models import AUser
from friends.models import FriendList, FriendRequest
from .models import UserProfile,LearningSource

# from notifications.signals import notify
from notification.utilities import notify,allNotifications

@login_required(login_url="login")
def home(request):
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()

	return render(request,"main/dashboard.html",context)

@login_required(login_url="login")
def profile(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/profile.html",context)

@login_required(login_url="login")
def profileSpecific(request,username):
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	context['isFriend']=False
	context['friendRequestPending']=False

	otherUser=AUser.objects.get(username=username)
	userFriendList=FriendList.objects.get(user=request.user)

	if userFriendList.isFriend(otherUser):
		context['isFriend']=True
	elif FriendRequest.objects.filter(sender=request.user, receiver=otherUser, isActive=True):
		context['friendRequestPending']=True
	try:
		context['profile']=UserProfile.objects.get(url=username)
	except:
		pass
	return render(request,"main/func/profileSpecific.html",context)

@login_required(login_url="login")
def editProfile(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)

	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()

	if request.method=="POST":
		displayName=request.POST.get("display_name")
		shortDescription=request.POST.get("short_bio")
		longDescription=request.POST.get("long_bio")
		gender=request.POST.get("gender")
		# print("Fetched the values")

		user_profile = UserProfile.objects.get(user=request.user)
		# print("Object fetched")

		if request.FILES.get('avatar'):
			avatar_file = request.FILES['avatar']
			# print("avatar fetched, about to change")
			user_profile.avatar.save(avatar_file.name, avatar_file)
		if displayName!=None:
			# print("Changed display name")
			user_profile.display_name = displayName
		if shortDescription!=None:
			# print("Changed short bio")
			user_profile.short_bio = shortDescription
		if longDescription!=None:
			# print("changed long bio")
			user_profile.long_bio = longDescription
		if gender!=None:
			user_profile.gender=gender.upper()

		user_profile.save()
		return render(request,'main/func/profile.html',context)

	

	return render(request,'main/edit/editProfile.html',context)
@login_required(login_url="login")
def notifications(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/notifications.html",context)



@login_required(login_url="login")
def feedback(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/feedback.html",context)


@login_required(login_url="login")
def contact(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/contact.html",context)


@login_required(login_url="login")
def events(request):
	context={}
	# user = models.AUser.objects.get(pk=request.user.pk)
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	# notify(request.user,"You Just Visited the Events section","Its a working notification! But a test notification however...",link="https://www.google.com/")
	# notify.send(request.user, recipient=request.user, verb='you just visited the events section',description='WOOOHOO! Its a working notification, though its a test notification, its cool!')
	# Notification.objects.create(recipient=request.user, message="You just viewed the Events Page!")

	context['learning_sources']=LearningSource.objects.all()
	return render(request,"main/func/events.html",context)



@login_required(login_url="login")
def settings(request):
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/settings.html",context)



@login_required(login_url="login")
def startQuiz(request):
	context={}
	context['notifications_unread']=allNotifications(request.user.pk)
	context['notifications_count']=allNotifications(request.user.pk).count()
	return render(request,"main/func/quiz.html",context)

def logOut(request):
	logout(request)
	return redirect("/login/")

# 