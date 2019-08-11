from typing import Optional

from django.db import models

from common.models import Game
from tic_tac_toe.models import GameTTT


class GameUTTT(Game):
    game = models.ForeignKey(GameTTT, on_delete=models.CASCADE, related_name='uttt_game', null=True)
    prev_i = models.IntegerField(default=0)
    prev_j = models.IntegerField(default=0)

    WIDTH = 9
    HEIGHT = 9

    @classmethod
    def new_game(cls, p1, p2):
        game = GameTTT(p1=p1, p2=p2)
        game.save()
        g = cls(p1=p1, p2=p2)
        g.save()

        for i in range(3):
            for j in range(3):
                child = GameUTTT_ChildGame.new_game(g, i, j)
                if child is not None:  # implement some kind of abort?
                    child.play_id = g.id
                    child.play_url = 'uttt:play'
                    child.save()
        return g

    def play(self, i: int, j: int) -> bool:
        # g = GameTTT.objects.get(id=fk)
        try:
            g = GameUTTT_ChildGame.get_game(self, row=self.prev_i, col=self.prev_j)
            if g.play(i, j, player=self.player):
                if g.winner != 0:
                    if not self.game.play(self.prev_i, self.prev_j, player=self.player):
                        raise Exception

                    if self.game.winner != 0:
                        self.winner = self.game.winner
                        for game in GameTTT.objects.filter(play_id=self.pk):
                            game.game_over = True
                            game.save()

                self.game_over = self.game.game_over
                self.prev_i = i
                self.prev_j = j
                self.toggle_player()
                g.save()
                self.save()
                return True
            else:
                return False
        except (models.ObjectDoesNotExist, Exception):
            return False

    def pick(self, row: int, col: int, i: int, j: int) -> bool:
        self.prev_i = row
        self.prev_j = col
        return self.play(i, j)

    def game_list(self) -> list:
        game_list = GameUTTT_ChildGame.objects.filter(id_parent=self.pk)
        g = [[None for i in range(3)] for j in range(3)]
        for game in game_list:
            g[game.row][game.col] = game.game
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
