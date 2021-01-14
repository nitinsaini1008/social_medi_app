import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import chatmsg
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
        room_name=text_data_json['room_name']
        print(room_name)
        user=text_data_json['username']
        other=text_data_json['other']
        print(user)
        u=User.objects.get(username=user)
        u2=User.objects.get(username=other)
        print(u.email)
        print(message)
        m=chatmsg(roomname=room_name,by_user=u,to_user=u2,msg=message)
        m.save()
        d={'username':u.username,'photo':u.first_name}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'by_user':u.username,
                'photo':u.first_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        u=event['by_user']
        p=event['photo']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'by_user':u,
            'photo':p
        }))