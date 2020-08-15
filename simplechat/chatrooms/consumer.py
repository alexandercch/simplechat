import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatRoomConsumer(WebsocketConsumer):

    def connect(self):
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
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json_data['message']
            }
        )

    def chat_message(self, event):
        data = json.dumps({'message': event['message']})
        self.send(text_data=data)
