import json
from asgiref.sync import async_to_sync
import redis

from django.conf import settings

from channels.generic.websocket import WebsocketConsumer
from .constants import STOCK_COMMAND
from .tasks import retrieve_stock_value


class ChatRoomConsumer(WebsocketConsumer):
    """
    websocket library, connect creates chat room, receive receive a message,
    user_message and bot_message send message to the group
    """

    http_user = True

    def connect(self):
        self.logged_in_user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['roomid']
        self.room_group_name =  "room_{}".format(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']
        if message.startswith(STOCK_COMMAND):
            retrieve_stock_value.delay(self.room_group_name, message)
        else:
            username = self.logged_in_user.username
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_message',
                    'message': message,
                    'username': username
                }
            )
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
            msg = json.dumps({'message': message, 'username': username})
            r.lpush(self.room_group_name, msg)


    def user_message(self, event):
        msg = "{} :: {}".format(event['username'], event['message'])
        data = json.dumps({'message': msg })
        self.send(text_data=data)


    def bot_message(self, event):
        msg = "bot :: {}".format(event['message'])
        data = json.dumps({'message': msg })
        self.send(text_data=data)
