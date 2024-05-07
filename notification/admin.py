from django.contrib import admin
from .models import NotificationList,Notification

# Register your models here.

admin.site.register(NotificationList)
admin.site.register(Notification)