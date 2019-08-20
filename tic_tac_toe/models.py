from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import DataCell, Game
from common.templatetags.tags import icon


class GameTTT(Game):
    keep_score = models.BooleanField(_('keep_score'), default=True)
    play_id = models.IntegerField(_('play_id'), default=0)
    play_url = models.CharField(_('play_url'), default='ttt:play', max_length=100)

    WIDTH = 3
    HEIGHT = 3

    @classmethod
    def new_game(cls, p1, p2):
        g = cls(p1=p1, p2=p2)
        g.save()
        g.play_id = g.pk
        g.save()
        return g

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

    def field(self):
        conv = {1: icon('clear', 'round'), 2: icon('fiber_manual_record', 'outlined')}
        field = [['' for j in range(3)] for i in range(3)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = conv[e.data]
        return field
