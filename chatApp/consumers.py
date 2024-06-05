from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from authApp.models import User
from . import models

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_name = f"chat_{self.sender_id}_{self.receiver_id}"        
        # print("websocket Connect...",event)
        print("Channel Layer",self.channel_layer)
        print("Channel Name", self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def receive(self, text_data):
        token = text_data
        sender = User.objects.get(id=self.sender_id)
        recipient = User.objects.get(id=self.receiver_id)
        if sender.team.id != recipient.team.id:
            error= {'error': "Receiver not matches in your team...."}
            self.send(text_data=json.dumps(error))
            return
        conversation = models.conversation.objects.create(conversation_type="individual")
        message = models.messages.objects.create(sender=sender, receiver=recipient, content=token, conversation=conversation)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': message.sender.username
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    def disconnect(self, event):
        print("websocket Disconnect...",event)
        print("Channel Layer", self.channel_layer)
        print("Channel Name", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
