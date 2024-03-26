from django.shortcuts import render
from notifications.signals import notify
from django.http import HttpResponse
from notifications.models import Notification
# Create your views here.

def events(request):
    
	notify.send(request.user, recipient=request.user, verb='you just visited the events section',description='WOOOHOO! Its a working notification, though its a test notification, its cool!')
	return render(request, "main/func/events.html")

def deleteNotif(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.delete()
            return HttpResponse("Success")
        except Exception as E:
            return HttpResponse("Notification not found")
    else:
    	# pass
        return HttpResponse("Not allowed", status=405)