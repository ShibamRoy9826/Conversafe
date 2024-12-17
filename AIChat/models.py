from django.db import models
from landing.models import AUser

class AIRoom(models.Model):
    slug=models.SlugField(unique=True)
    user=models.ForeignKey(AUser,related_name="ai_chat_room",on_delete=models.CASCADE, null=True,blank=True)
    userConnected=models.BooleanField(default=False)

class Message(models.Model):
    room=models.ForeignKey(AIRoom,related_name="AIMessages",on_delete=models.CASCADE)
    user=models.ForeignKey(AUser,related_name="AIMessages",on_delete=models.CASCADE, null=True,blank=True)
    displayName=models.CharField(max_length=30,default="ErrorOnDisplay")
    content=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    NORMAL="NORMAL"
    JOINED="JOINED"
    LEFT="LEFT"
    SUGGEST="SUGEST"

    TYPES = (
        (NORMAL, "Normal"),
        (JOINED, "Joined"),
        (LEFT, "Left"),
        (SUGGEST, "Suggest")

    )

    messageType=models.CharField(max_length=6,
                  choices=TYPES,default="NORMAL")

    class Meta:
        ordering=('time',)
