import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import chatRoom,Message
from landing.models import AUser
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name=self.scope['url_route']['kwargs']['room_name']
		self.room_group_name='chat_%s' % self.room_name


		self.user1Username=""
		self.user2Username=""
		self.user1Pfp=""
		self.user2Pfp=""
		self.user1Display=""
		self.user2Display=""
		self.userCount=0

		await self.increaseUserCount(self.room_name)

		await self.checkUserCount(self.room_name)
	   

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name)

		await self.accept()


	async def disconnect(self,code):
		await self.decreaseUserCount(self.room_name)

		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name)

	async def receive(self,text_data):

		data=json.loads(text_data)

		if data['eventType']=="":
			await self.processChat(data)
		else:

			eventType=data['eventType']

			if eventType == 'offer':
				offerer=data['offerer']

				# Sending offer to the desired client
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'offer_received',
						'data': {
							'offerer':offerer,
							'rtcMessage': data['data']['rtcMessage']
						}
					}
				)

			if eventType == 'answerToOffer':
				# Sending an answer back to the client who proposed the offer
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'offer_answered',
						'data': {
							'rtcMessage': data['data']['rtcMessage']
						}
					}
				)

			if eventType == 'ICEcandidate':
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'ICEcandidate',
						'data': {
							'rtcMessage': data['data']['rtcMessage']
						}
					}
				)



	async def processChat(self,data):
		message=data['message']
		username=data['username']
		displayname=data['displayName']
		room=data['room']
		messageType=data['messageType']

		if messageType=="JOINED":
			await self.addNewUser(self.room_name,username)
		elif messageType=="LEFT":
			await self.removeUser(self.room_name,username)

		await self.save_message(displayname,username,room,message,messageType)	

		await self.getUsers(self.room_name)


		await self.channel_layer.group_send(
			self.room_group_name,
			{
			'type':'chat_message',
			'displayName':displayname,
			'message':message,
			'username':username,
			'room':room,
			'messageType':messageType,
			'user1Username':self.user1Username,
			'user2Username':self.user2Username,
			'user1Display':self.user1Display,
			'user2Display':self.user2Display,
			'user1Pfp':self.user1Pfp,
			'user2Pfp':self.user2Pfp,
			'userCount':self.userCount
			})

	async def offer_received(self, event):

		await self.send(text_data=json.dumps({
			'eventType': 'offer_received',
			'data': event['data'],
			'messageType':'webRTC'
		}))


	async def offer_answered(self, event):
		await self.send(text_data=json.dumps({
			'eventType': 'offer_answered',
			'data': event['data'],
			'messageType':'webRTC'
		}))


	async def ICEcandidate(self, event):
		await self.send(text_data=json.dumps({
			'eventType': 'ICEcandidate',
			'data': event['data'],
			'messageType':'webRTC'
		}))

	async def chat_message(self,event):
		message=event['message']
		username=event['username']
		displayname=event['displayName']
		room=event['room']
		msgType=event['messageType']


		await self.getUsers(self.room_name)



		await self.send(text_data=json.dumps({
			'message':message,
			'displayName':displayname,
			'username':username,
			'room':room,
			'messageType':msgType,
			'user1Username':self.user1Username,
			'user2Username':self.user2Username,
			'user1Display':self.user1Display,
			'user2Display':self.user2Display,
			'user1Pfp':self.user1Pfp,
			'user2Pfp':self.user2Pfp,
			'userCount':self.userCount
			}))

	@sync_to_async
	def getUsers(self,room):
		obj=chatRoom.objects.get(slug=room)
		self.userCount=obj.users

		if obj.user1==None and obj.user2==None:
			self.user1Username=""
			self.user2Username=""
			self.user1Display=""
			self.user2Display=""
			self.user1Pfp=""
			self.user2Pfp=""
		elif obj.user1!=None and obj.user2==None:
			self.user1Username=obj.user1.username
			self.user2Username=""
			self.user1Pfp=obj.user1.userprofile.avatar.url
			self.user2Pfp=""
			self.user1Display=obj.user1.userprofile.display_name
			self.user2Display=""
		elif obj.user1==None and obj.user2!=None:
			self.user1Username=""
			self.user2Username=obj.user2.username
			self.user1Pfp=""
			self.user2Pfp=obj.user2.userprofile.avatar.url
			self.user2Display=obj.user2.userprofile.display_name
			self.user1Display=""
		else:
			self.user1Username=obj.user1.username
			self.user2Username=obj.user2.username
			self.user1Pfp=obj.user1.userprofile.avatar.url
			self.user2Pfp=obj.user2.userprofile.avatar.url
			self.user1Display=obj.user1.userprofile.display_name
			self.user2Display=obj.user2.userprofile.display_name
			

	@sync_to_async
	def checkUserCount(self,room):
		obj=chatRoom.objects.get(slug=room)
		if obj.users>2:
			return False

	@sync_to_async
	def addNewUser(self,room,username):
		obj=chatRoom.objects.get(slug=room)
		user=AUser.objects.get(username=username)

		if obj.user1!=user and obj.user2!=user:
			if obj.user1==None and obj.user2==None:
				obj.user1=user
			elif obj.user1==None:
				obj.user1=user
			elif obj.user2==None:
				obj.user2=user


		obj.save()

	@sync_to_async
	def removeUser(self,room,username):
		obj=chatRoom.objects.get(slug=room)
		if obj.users==1:
			obj.user1=None
			obj.user2=None

		elif obj.user1!=None:
			if username==obj.user1.username:
				obj.user1=None
			else:
				obj.user2=None
		elif obj.user2!=None:
			if username==obj.user2.username:
				obj.user1=None

			else:
				obj.user2=None
		else:
			obj.user1=None
			obj.user2=None


		obj.save()

	@sync_to_async
	def increaseUserCount(self,room):
		obj=chatRoom.objects.get(slug=room)
		obj.users+=1
		self.userCount+=1
		obj.lastActive=timezone.now()
		obj.save()

	@sync_to_async
	def decreaseUserCount(self,room):
		obj=chatRoom.objects.get(slug=room)
		obj.users-=1
		self.userCount-=1
		obj.lastActive=timezone.now()
		obj.save()


	@sync_to_async
	def save_message(self,display,username,room,message,messageType):
		user=AUser.objects.get(username=username)
		roomName=chatRoom.objects.get(slug=room)

		Message.objects.create(displayName=display,user=user,room=roomName,content=message,messageType=messageType)

