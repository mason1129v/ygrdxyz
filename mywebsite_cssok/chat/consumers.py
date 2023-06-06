import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync



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
        if message == '想看鞋子':
            print('cope')
            data = {
                'type': 'redirect',
                'url': '/client_sp/?keyword=' + 'shoe',  # Replace '/some-url/' with the desired URL to redirect to
                'value': 'shoe'  # Replace 'example' with the value you want to pass
            }
            self.send(text_data=json.dumps(data))
            print(data)
        elif message == '想看衣服':
            print('cope')
            data = {
                'type': 'redirect',
                'url': '/client_sp/?keyword=' + 'cloth',  # Replace '/some-url/' with the desired URL to redirect to
                'value': 'cloth'  # Replace 'example' with the value you want to pass
            }
            self.send(text_data=json.dumps(data))
            print(data)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                # 'randomName': self.random_name,
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            # 'randomName' : random_name,
            'message': message
        }))

