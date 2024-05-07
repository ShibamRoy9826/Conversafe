from django.contrib import admin
from .models import chatRoom,ReportedMessage
# Register your models here.

admin.site.register(chatRoom)
admin.site.register(ReportedMessage)
# admin.site.register(Message)