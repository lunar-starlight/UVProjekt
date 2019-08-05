from django.db import models

from common.models import DataCell, Game
from common.templatetags.tags import icon


class GameTTT(Game):
    keep_score = models.BooleanField(default=True)
    play_id = models.IntegerField(default=0)
    play_url = models.CharField(default='ttt:play', max_length=100)

    WIDTH = 3
    HEIGHT = 3

    def check_win(self, i: int, j: int) -> bool:
        if self.get_data(0, j) == self.get_data(1, j) == self.get_data(2, j) or self.get_data(i, 0) == self.get_data(i, 1) == self.get_data(i, 2):
            return True
        if i == j:
            if self.get_data(0, 0) == self.get_data(1, 1) == self.get_data(2, 2):
                return True
        if i == 2-j:
            if self.get_data(0, 2) == self.get_data(1, 1) == self.get_data(2, 0):
                return True
        return False

    def play(self, i: int, j: int, player: int = None) -> bool:
        return super().play(i, j, player=player)

    def field(self):
        conv = {1: icon('times', 'solid'), 2: icon('circle', 'regular')}
        field = [['' for j in range(3)] for i in range(3)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = conv[e.data]
        return field
