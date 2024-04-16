import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import AIRoom,Message
from landing.models import AUser
from django.utils import timezone

import random
# Gemini
import google.generativeai as genai


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name=self.scope['url_route']['kwargs']['room_name']
		self.room_group_name='chat_%s' % self.room_name

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name)

		await self.accept()

		genai.configure(api_key = "AIzaSyDFS_hhrIxPmD8qrag30FH7ltuKvpzegx4")
		model = genai.GenerativeModel('gemini-pro')
		self.chat = model.start_chat(history=[])


	async def disconnect(self,code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name)

	async def receive(self,text_data):
		data=json.loads(text_data)

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

		await self.channel_layer.group_send(
			self.room_group_name,
			{
			'type':'chat_message',
			'displayName':displayname,
			'message':message,
			'username':username,
			'room':room,
			'messageType':messageType,
			})

		if messageType=="JOINED":
			await self.channel_layer.group_send(
				self.room_group_name,
				{
				'type':'send_initial',
				'displayName':"Mr. AI",
				'userPrompt':displayname,
				'username':"Mr AI",
				'room':room,
				'messageType':'NORMAL'

				})
		
		if messageType=="NORMAL":
			await self.channel_layer.group_send(
				self.room_group_name,
				{
				'type':'ai_reply',
				'displayName':"Mr. AI",
				'userPrompt':message,
				'username':"Mr AI",
				'room':room,
				'messageType':'NORMAL'
				})

	async def ai_reply(self,event):
		def cleanReply(text):
			if "X 20 20 px" in text:
				text=text.replace("X 20 20 px","")
			if "*" in text:
				text=text.replace('*',"")
			return text
		error=False
		userPrompt=event['userPrompt']
		AiUsername=event['username']
		AiDisplayname=event['displayName']
		room=event['room']
		msgType=event['messageType']

		try:
			self.chat.send_message(userPrompt)
			AiReply=self.chat.history[-1].parts[0].text
			AiReply=cleanReply(AiReply)
		except:
			print("Error Occured...")
			AiReply==""
			error=True
		

		await self.save_message(AiDisplayname,AiUsername,room,AiReply,msgType)	

		await self.send(text_data=json.dumps({
			'message':AiReply,
			'displayName':AiDisplayname,
			'username':AiUsername,
			'room':room,
			'messageType':msgType,
			'initial':'no'
			}))


	async def send_initial(self,event):
		userPrompt=event['userPrompt']
		AiUsername=event['username']
		AiDisplayname=event['displayName']
		room=event['room']
		msgType=event['messageType']
		replies=["Hey there!  What's going on today? 😃","You seem like an interesting person... tell me something unexpected! ✨","What secret talents are you hiding? I won't tell a soul!😊"]
		AiReply=random.choice(replies)

		await self.save_message(AiDisplayname,AiUsername,room,AiReply,msgType)	
		
		await self.send(text_data=json.dumps({
			'message':AiReply,
			'displayName':AiDisplayname,
			'username':AiUsername,
			'room':room,
			'messageType':msgType,
			'initial':'yes'
			}))

	async def chat_message(self,event):
		message=event['message']
		username=event['username']
		displayname=event['displayName']
		room=event['room']
		msgType=event['messageType']

		await self.send(text_data=json.dumps({
			'message':message,
			'displayName':displayname,
			'username':username,
			'room':room,
			'messageType':msgType,
			'initial':'no'
			}))


	@sync_to_async
	def addNewUser(self,room,username):
		obj=AIRoom.objects.get(slug=room)
		user=AUser.objects.get(username=username)
		obj.userConnected=True
		obj.save()

	@sync_to_async
	def removeUser(self,room,username):
		obj=AIRoom.objects.get(slug=room)
		user=AUser.objects.get(username=username)
		obj.userConnected=False
		obj.save()


	@sync_to_async
	def save_message(self,display,username,room,message,messageType):
		roomName=AIRoom.objects.get(slug=room)

		Message.objects.create(displayName=display,room=roomName,content=message,messageType=messageType)

