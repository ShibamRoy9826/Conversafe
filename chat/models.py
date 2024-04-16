from django.db import models
from landing.models import AUser
from django.utils import timezone

# Create your models here.

class chatRoom(models.Model):
	name=models.CharField(max_length=255)
	slug=models.SlugField(unique=True)
	users=models.IntegerField(default=0)

	# user1=models.CharField(max_length=320,null=True,blank=True)
	# user2=models.CharField(max_length=320,null=True,blank=True)

	user1=models.ForeignKey(AUser,related_name="chat_room",on_delete=models.CASCADE,null=True, blank=True)

	user2=models.ForeignKey(AUser,related_name="chat_room_user2",on_delete=models.CASCADE,null=True, blank=True)

	lastActive=models.DateTimeField(default=timezone.now)
	
	MALE="MALE"
	FEMALE="FEMALE"
	OTHER="OTHER"

	GENDERS = (
		(MALE, "Male"),
		(FEMALE, "Female"),
		(OTHER, "Other")
	)
	
	gender=models.CharField(max_length=6,
				  choices=GENDERS,null=True,blank=True)



class Message(models.Model):

	room=models.ForeignKey(chatRoom,related_name="messages",on_delete=models.CASCADE)
	user=models.ForeignKey(AUser,related_name="messages",on_delete=models.CASCADE)
	displayName=models.CharField(max_length=30,default="ErrorOnDisplay")
	content=models.TextField()
	time=models.DateTimeField(auto_now_add=True)
	NORMAL="NORMAL"
	JOINED="JOINED"
	LEFT="LEFT"

	TYPES = (
		(NORMAL, "Normal"),
		(JOINED, "Joined"),
		(LEFT, "Left")

	)

	messageType=models.CharField(max_length=6,
				  choices=TYPES,default="NORMAL")

	class Meta:
		ordering=('time',)