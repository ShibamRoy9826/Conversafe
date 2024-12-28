###  Libraries and stuff ############################################################
import json
import random  # For random initial messages
from requests import get,post

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from gtts import gTTS
from pygame import mixer
from transformers import BlenderbotForConditionalGeneration  # For AI Models
from transformers import BlenderbotTokenizer

# For Spellchecker
from spellchecker import SpellChecker

from landing.models import AUser
# from core.models import UserProfile

# Some Model objects
from .models import AIRoom, Message

####################################################################################

mixer.init()
s=SpellChecker()
translateUrl= "http://127.0.0.1:5000/translate"
translateHeaders = {
    "Content-Type": "application/json"
}

def translate(txt,lang):
    data = {
        "q": "",
        "source": "en",
        "target": lang,
        "format": "text",
        "api_key": ""
    }
    response = post(translateUrl, data=json.dumps(data), headers=translateHeaders)


class ChatConsumer(AsyncWebsocketConsumer):
    # Connecting client with server
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Initializing the bot
        self.tokenizer = BlenderbotTokenizer.from_pretrained(
            "facebook/blenderbot-400M-distill"
        )
        self.model = BlenderbotForConditionalGeneration.from_pretrained(
            "facebook/blenderbot-400M-distill"
        )
        print("Bot initialization completed!")

    # Handles Chat prompts with the model
    def chat(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        reply = self.model.generate(**inputs)
        return self.tokenizer.decode(reply[0], skip_special_tokens=True)

    # Disconnects client from server
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receiving data from client to server
    async def receive(self, text_data):
        # Storing all received data
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        displayname = data["displayName"]
        room = data["room"]
        messageType = data["messageType"]

        # Checking Message type for further processing
        if messageType == "JOINED":
            await self.addNewUser(self.room_name, username)
        elif messageType == "LEFT":
            await self.removeUser(self.room_name, username)

        # Saving Received message
        await self.save_message(displayname, username, room, message, messageType)

        # Sending back the message to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "displayName": displayname,
                "message": message,
                "username": username,
                "room": room,
                "messageType": messageType,
            },
        )
        if messageType=="NORMAL":
            errors=s.unknown(message.split(" "))
            corrections=[]
            for i in errors:
                corrections.append(s.correction(i))

            if len(errors)!=0:
                msg="Some corrections to the last sentence:<br><ul class='flex flex-col'>"
                for ind,i in enumerate(errors):
                    if msg!=f"<li>  -> i</li>":
                        msg+=f"<li style='list-style-type: circle;margin-left: 1rem;'> {i} -> {corrections[ind]}</li>"
                msg+="</ul>"
                print(msg)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "displayName": "Corrections",
                        "message": msg,
                        "username": username,
                        "room": room,
                        "messageType": "SUGGEST",
                    },
                )

        # Sending Initial message on joining and giving reply to any prompt
        if messageType == "JOINED":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_initial",
                    "displayName": "AI",
                    "userPrompt": displayname,
                    "username": "Mr AI",
                    "room": room,
                    "messageType": "NORMAL",
                },
            )

        if messageType == "NORMAL":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "ai_reply",
                    "displayName": "AI",
                    "userPrompt": message,
                    "username": "Mr AI",
                    "room": room,
                    "messageType": "NORMAL",
                },
            )

    # Generating reply by the AI Model
    async def ai_reply(self, event):
        def cleanReply(text):
            if "X 20 20 px" in text:
                text = text.replace("X 20 20 px", "")
            if "*" in text:
                text = text.replace("*", "")

            return text

        error = False
        userPrompt = event["userPrompt"]
        AiUsername = event["username"]
        AiDisplayname = event["displayName"]
        room = event["room"]
        msgType = event["messageType"]

        AiReply = self.chat(userPrompt)
        AiReply = cleanReply(AiReply)


        try:
            a = gTTS(AiReply, lang="en")
            a.save("temp/temp.mp3")
            mixer.music.load("temp/temp.mp3")
            mixer.music.play()
        except Exception as e:
            print("GTTS ERROR: ",e)

        await self.save_message(AiDisplayname, AiUsername, room, AiReply, msgType)

        await self.send(
            text_data=json.dumps(
                {
                    "message": AiReply,
                    "displayName": AiDisplayname,
                    "username": AiUsername,
                    "room": room,
                    "messageType": msgType,
                    "initial": "no",
                }
            )
        )

    # Initial greeting
    async def send_initial(self, event):
        userPrompt = event["userPrompt"]
        AiUsername = event["username"]
        AiDisplayname = event["displayName"]
        room = event["room"]
        msgType = event["messageType"]
        replies = [
            "Hey there!  What's going on today? 😃",
            "You seem like an interesting person... tell me something unexpected! ✨",
            "What secret talents are you hiding? I won't tell a soul!😊",
            "Hello! What’s on your mind today? ",
            "Hey! I’m here to help, chat, or just listen. What’s up? ",
            "Did you know an octopus has three hearts? What’s a fun fact you know? ",
        ]
        AiReply = random.choice(replies)
        print("Ai send initial choice: ",AiReply)
        try:
            a = gTTS(AiReply[:-1], lang="en")
            a.save("temp/temp.mp3")
            mixer.music.load("temp/temp.mp3")
            mixer.music.play()
        except Exception as e:
            print("ERROR: ",e)

        await self.save_message(AiDisplayname, AiUsername, room, AiReply, msgType)

        await self.send(
            text_data=json.dumps(
                {
                    "message": AiReply,
                    "displayName": AiDisplayname,
                    "username": AiUsername,
                    "room": room,
                    "messageType": msgType,
                    "initial": "yes",
                }
            )
        )
        print("Sent message from the server")

    # Function that handles sending messages to client
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        displayname = event["displayName"]
        room = event["room"]
        msgType = event["messageType"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "displayName": displayname,
                    "username": username,
                    "room": room,
                    "messageType": msgType,
                    "initial": "no",
                }
            )
        )

    ######## Important functions ##############################################
    @sync_to_async
    def addNewUser(self, room, username):
        obj = AIRoom.objects.get(slug=room)
        user = AUser.objects.get(username=username)
        obj.userConnected = True
        print("New user connected!")
        obj.save()

    @sync_to_async
    def removeUser(self, room, username):
        obj = AIRoom.objects.get(slug=room)
        user = AUser.objects.get(username=username)
        obj.userConnected = False
        obj.save()

    @sync_to_async
    def save_message(self, display, username, room, message, messageType):
        roomName = AIRoom.objects.get(slug=room)

        Message.objects.create(
            displayName=display, room=roomName, content=message, messageType=messageType
        )
