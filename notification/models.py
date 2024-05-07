from django.db import models
from landing.models import AUser

class Notification(models.Model):
	title=models.CharField(max_length=100)
	desc=models.CharField(max_length=500)
	link=models.CharField(max_length=500,blank=True,null=True)
	timestamp=models.DateTimeField(auto_now_add=True)
	
class NotificationList(models.Model):
	user=models.OneToOneField(AUser,on_delete=models.CASCADE,related_name="user_notification_list")
	notifications=models.ManyToManyField(Notification, blank=True,related_name="notifications")
	count=models.IntegerField(default=0)

	def __str__(self):
		return self.user.username

	def notify(self,notification):
		self.notifications.add(notification)
		self.count+=1
		self.save()

	def deleteNotification(self,notificationId):
		notification = Notification.objects.get(pk=notificationId)
		self.notifications.remove(notification)
		self.count-=1

	def messages(self):
		return self.notifications.all()

	def allCount(self):
		return self.count
