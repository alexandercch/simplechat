import json
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from .constants import STOCK_COMMAND
from .tasks import retrieve_stock_value


class ChatRoomConsumer(WebsocketConsumer):

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
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_message',
                    'message': message,
                    'username': self.logged_in_user.username
                }
            )


    def user_message(self, event):
        msg = "{} > {}".format(event['username'], event['message'])
        data = json.dumps({'message': msg })
        self.send(text_data=data)


    def bot_message(self, event):
        msg = "bot > {}".format(event['message'])
        data = json.dumps({'message': msg })
        self.send(text_data=data)
