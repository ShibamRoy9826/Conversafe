from notification.models import NotificationList,Notification
from landing.models import AUser

def notify(recepient,Title,Desc,link=""):
	newNotif=Notification.objects.create(title=Title,desc=Desc,link=link)
	notificationList=NotificationList.objects.get(user=recepient)
	notificationList.notify(newNotif)

def deleteNotification(User,NotifId):
	notificationList=NotificationList.objects.get(user=User)

	notificationList.deleteNotification(NotifId)


def allNotifications(userID):
	u=AUser.objects.get(pk=userID)
	notifList=NotificationList.objects.get(user=u)
	return notifList.messages()