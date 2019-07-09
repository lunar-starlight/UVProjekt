from django.db import models

from tic_tac_toe.models import Game as GameTTT, Player


class GameUTTT(models.Model):
    g0 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g0')
    g1 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g1')
    g2 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g2')
    g3 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g3')
    g4 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g4')
    g5 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g5')
    g6 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g6')
    g7 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g7')
    g8 = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_g8')
    p1 = models.ForeignKey(Player, related_name='uttt_p1', on_delete=models.DO_NOTHING, default=0)
    p2 = models.ForeignKey(Player, related_name='uttt_p2', on_delete=models.DO_NOTHING, default=0)
    prev_i = models.IntegerField(default=0)
    prev_j = models.IntegerField(default=0)
    player = models.IntegerField(default=1)
    game = models.OneToOneField(GameTTT, on_delete=models.CASCADE, related_name='uttt_game')

    games = list()

    def setup(self):
        self.g0 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g1 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g2 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g3 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g4 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g5 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g6 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g7 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.g8 = GameTTT(p1=self.p1, p2=self.p2, keep_score=False)
        self.game = GameTTT(p1=self.p1, p2=self.p2)

        self.games = [g0.id, g1.id, g2.id, g3.id, g4.id, g5.id, g6.id, g7.id, g8.id]

    def toggle_player(self) -> None:
        self.player = 3 - self.player

    def play(self, i: int, j: int) -> bool:
        p = self.game.get_position(i, j)
        if p is None:
            return False
        
        g = GameTTT.objects.get(id=self.games[p])
        g.play(i, j, player=self.player)

        if g.winner != 0:
            self.game.place(i, j, player=self.player)

        self.prev_i = i
        self.prev_j = j
        self.toggle_player()
