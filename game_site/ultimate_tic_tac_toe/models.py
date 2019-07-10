from django.db import models

from tic_tac_toe.models import Game as GameTTT, Player


class GameUTTT(models.Model):
    g0 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g0')
    g1 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g1')
    g2 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g2')
    g3 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g3')
    g4 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g4')
    g5 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g5')
    g6 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g6')
    g7 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g7')
    g8 = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_g8')
    p1 = models.ForeignKey(Player, related_name='uttt_p1', on_delete=models.DO_NOTHING, default=0)
    p2 = models.ForeignKey(Player, related_name='uttt_p2', on_delete=models.DO_NOTHING, default=0)
    prev_i = models.IntegerField(default=0)
    prev_j = models.IntegerField(default=0)
    player = models.IntegerField(default=1)
    game = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_game')

    games = list()

    def toggle_player(self) -> None:
        self.player = 3 - self.player

    def play(self, i: int, j: int) -> bool:
        p = self.game.get_position(i, j)
        if p is None:
            return False
        
        # pp = self.game.get_position(self.prev_i, self.prev_j)
        # self.games = [self.g0.id, self.g1.id, self.g2.id, self.g3.id, self.g4.id, self.g5.id, self.g6.id, self.g7.id, self.g8.id]
        g = GameTTT.objects.get(id=fk)
        g.play(i, j, player=self.player)

        if g.winner != 0:
            self.game.play(i, j, player=self.player)

        self.prev_i = i
        self.prev_j = j
        self.toggle_player()
        self.save()
