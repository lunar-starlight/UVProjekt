import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_pk = self.scope['url_route']['kwargs']['pk']
        self.game_group_name = f'game_{self.game_pk}'

        # Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        player = text_data_json['player']
        i = text_data_json['i']
        j = text_data_json['j']

        # Send message to game group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'game_move',
                'player': player,
                'i': i,
                'j': j,
            }
        )

    def game_move(self, event):
        player = event['player']
        i = event['i']
        j = event['j']

        self.send(text_data=json.dumps({
            'player': player,
            'i': i,
            'j': j,
        }))
