from typing import Optional

from django.conf import settings
from django.db import models

from tic_tac_toe.models import GameTTT


class GameUTTT(models.Model):
    p1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uttt_p1', on_delete=models.DO_NOTHING, default=0)
    p2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uttt_p2', on_delete=models.DO_NOTHING, default=0)
    prev_i = models.IntegerField(default=0)
    prev_j = models.IntegerField(default=0)
    player = models.IntegerField(default=1)
    game = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_game', null=True)

    def toggle_player(self) -> None:
        self.player = 3 - self.player

    def current_player(self):
        if self.player == 1:
            return self.p1
        else:
            return self.p2

    def play(self, i: int, j: int) -> bool:
        # g = GameTTT.objects.get(id=fk)
        try:
            g = GameUTTT_ChildGame.get_game(self, row=self.prev_i, col=self.prev_j)
            if g.play(i, j, player=self.player):
                if g.winner != 0:
                    if not self.game.play(self.prev_i, self.prev_j, player=self.player):
                        raise Exception

                    if self.game.winner != 0:
                        for game in GameTTT.objects.filter(play_id=self.pk):
                            game.game_over = True
                            game.save()

                self.prev_i = i
                self.prev_j = j
                self.toggle_player()
                g.save()
                self.save()
        except (models.ObjectDoesNotExist, Exception):
            pass

    def pick(self, row: int, col: int, i: int, j: int) -> bool:
        self.prev_i = row
        self.prev_j = col
        self.play(i, j)

    def games(self) -> list:
        g = list()
        for i in range(3):
            t = list()
            for j in range(3):
                t.append(GameUTTT_ChildGame.get_game(self, row=i, col=j))
            g.append(t)
        return g


class GameUTTT_ChildGame(models.Model):
    id_parent = models.ForeignKey(GameUTTT, on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    game = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_child_game')

    @classmethod
    def new_game(cls, parent: GameUTTT, i: int, j: int) -> Optional[GameTTT]:
        g: GameTTT
        try:
            g = GameTTT(p1=parent.p1, p2=parent.p2, keep_score=False)
            g.save()
        except models.ObjectDoesNotExist:
            return None

        try:
            obj = GameUTTT_ChildGame(id_parent=parent, row=i, col=j, game=g)
            obj.save()
        except models.ObjectDoesNotExist:
            g.delete()
            return None
        return g

    @classmethod
    def get_game(cls, parent: GameUTTT, row: int, col: int) -> Optional[GameTTT]:
        try:
            g = GameUTTT_ChildGame.objects.get(id_parent=parent, row=row, col=col)
            return g.game
        except models.ObjectDoesNotExist:
            return None
