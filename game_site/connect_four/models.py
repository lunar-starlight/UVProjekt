from django.db import models

from tic_tac_toe.models import Player

class GameCF(models.Model):
    player = models.IntegerField(default=1)
    winner = models.IntegerField(default=0)
    p1 = models.ForeignKey(Player, related_name='ttt_p1', on_delete=models.DO_NOTHING, default=0, null=True)
    p2 = models.ForeignKey(Player, related_name='ttt_p2', on_delete=models.DO_NOTHING, default=0, null=True)
    game_over = models.BooleanField(default=False)

    def get_position(self, i: int, j: int) -> Optional[int]:
        if i < 0 or j < 0 or i > 2 or j > 2:
            return None
        return 3*i + j

class DataCell(models.Model):
    id_game = models.ForeignKey(GameCF, on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    data = models.IntegerField(default=0)
