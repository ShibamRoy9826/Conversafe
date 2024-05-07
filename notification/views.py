from django.shortcuts import render
from django.http import HttpResponse
from .utilities import notify,deleteNotification
# Create your views here.

def events(request):
	# newNotif=Notification.objects.create(title="You Just Visited the Events section",desc="Its a working notification! But a test notification however...",link="https://www.google.com/")
	# notificationList=NotificationList.objects.get(user=request.user)
	# notificationList.notify(newNotif)

	# notify(request.user,"You Just Visited the Events section","Its a working notification! But a test notification however...",link="https://www.google.com/")
	
	return render(request, "main/func/events.html")

def deleteNotif(request):
	if request.method == 'POST':
		notification_id = request.POST.get('notification_id')
		try:
			deleteNotification(request.user,notification_id)
			return HttpResponse("Success")
		except Exception as E:
			print("Some Serious issue occured")
			print(E)
			return HttpResponse("Notification not found")
	else:
		# pass
		return HttpResponse("Not allowed", status=405)