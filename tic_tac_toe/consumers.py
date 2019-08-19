import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from common.models import Game
from tic_tac_toe.models import GameTTT
from ultimate_tic_tac_toe.models import GameUTTT
from connect_four.models import GameCF


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
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
        game = text_data_json['game']
        player = text_data_json['player']
        i = text_data_json.get('i', None)
        j = text_data_json.get('j', None)
        row = text_data_json.get('row', None)
        col = text_data_json.get('col', None)
        g: Game = Game.objects.get(pk=game)
        if self.user != g.current_player():
            return

        # Send message to game group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'game_move',
                'game': game,
                'player': player,
                'i': i,
                'j': j,
                'row': row,
                'col': col,
            }
        )

    # Receive message from room group
    def game_move(self, event):
        game = event['game']
        player = event['player']
        i = event.get('i', None)
        j = event.get('j', None)
        row = event.get('row', None)
        col = event.get('col', None)

        g: Game = Game.objects.get(pk=game)
        if self.user == g.current_player():
            if isinstance(g, GameUTTT) and g.is_free_pick():
                g.play(i, j, row, col)
            elif isinstance(g, GameTTT) or isinstance(g, GameUTTT):
                g.play(i, j)
            elif isinstance(g, GameCF):
                g.play(col)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'game': game,
            'player': player,
            'i': i,
            'j': j,
            'row': row,
            'col': col,
            'reload': g.game_over or g.p1.username == 'ai' or g.p2.username == 'ai',
        }))
