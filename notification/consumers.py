# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name="notification"
#         await self.channel_layer.group_add(self.group_name,self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         title = text_data_json['title']
#         time = text_data_json['time']
#         event={
#         'type':'send_notification',
#         'message':message,
#         'title':title,
#         'time':time
#         }

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.group_name,event
#         )

#     # Receive message from room group
#     async def send_notification(self, event):
#         message = event['message']
#         title=event['title']
#         time=event['time']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({'message':message,'title':title,'time':time}))