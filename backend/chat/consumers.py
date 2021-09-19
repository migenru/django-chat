# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import ChatMessage, ChatUser
from django.contrib.sessions.backends.db import SessionStore


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': self.scope["session"]["user_id"],
                'user_nickname': self.scope["session"]["user_nickname"],
            }
        )
        user_scope = ChatUser.objects.get(pk=self.scope["session"]["user_id"])
        ChatMessage.objects.create(user=user_scope, content=message)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_nickname = event['user_nickname']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_nickname': user_nickname,
        }))

