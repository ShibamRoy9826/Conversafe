from django.db import models
from landing.models import AUser
from notification.utilities import notify
# Create your models here.

class FriendList(models.Model):
	# Continue from here
	user=models.OneToOneField(AUser,on_delete=models.CASCADE,related_name="user_friend_list")
	friends=models.ManyToManyField(AUser, blank=True,related_name="friends")

	def __str__(self):
		return self.user.username
		
	def addFriend(self,profile):
		if not profile in self.friends.all():
			self.friends.add(profile)
			self.save()

	def removeFriend(self,profile):
		if profile in self.friends.all():
			self.friends.remove(profile)
			self.save()	

	def unfriend(self,removee):
		# Removing from own Friend List
		remover=self
		remover.removeFriend(removee)

		# Removing from the other user
		removeeList=FriendList.objects.get(user=removee)
		removeeList.removeFriend(remover.user)
		notify(removee,"You got unfriended 😭",f'{remover} removed you from their friendlist😢😢')


	def isFriend(self,user):
		if user in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	sender=models.ForeignKey(AUser, on_delete=models.CASCADE,related_name="sender")
	receiver=models.ForeignKey(AUser, on_delete=models.CASCADE,related_name="receiver")
	isActive=models.BooleanField(blank=True,null=False,default=True)
	time=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username

	def accept(self):
		receiverList=FriendList.objects.get(user=self.receiver)
		if receiverList:
			receiverList.addFriend(self.sender)

			senderList=FriendList.objects.get(user=self.sender)
			if senderList:
				senderList.addFriend(self.receiver)
				self.isActive=False
				self.save()

		notify(self.sender,'Your friend request got accepted!🥳',f'{self.receiver} is now your friend ✨✨')
		notify(self.receiver,'You just made a new friend!',f'{self.sender} is now your friend ✨✨')
	
	def decline(self):
		self.isActive=False
		self.save()

		notify(self.sender, 'Your Friend Request was declined😭',f'{self.receiver} declined your friend request😭')

	def cancel(self):
		self.isActive=False
		self.save()

		# notify(self.sender,"You cancelled your friend request",f' You cancelled your friend request to {self.receiver}')
