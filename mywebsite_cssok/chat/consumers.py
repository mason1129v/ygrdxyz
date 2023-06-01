import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import random


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        # self.random_name = self.get_random_name()
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']    
        
        print(message)
        print("=========")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                # 'randomName': self.random_name,
                'message':message
            }
        )


    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            # 'randomName' : random_name,
            'message': message
        }))

    def get_random_name(self):
        names = ["PIN", "DORRIS", "HUSI", "MASON"]
        return random.choice(names)