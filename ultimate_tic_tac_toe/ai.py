import random

from .models import GameUTTT, GameUTTT_ChildGame


class BaseAI(GameUTTT):

    class Meta:
        proxy = True

    def play(self, i: int, j: int, row: int = None, col: int = None) -> bool:
        if super().current_player().username != 'ai':
            b = super().play(i, j, row, col)
        self.player_num = self.player
        if self.game_over:
            return b
        else:
            return self.move()


class RandomUTTTAI(BaseAI):
    slug = 'random'

    class Meta:
        proxy = True

    def move(self):
        if GameUTTT_ChildGame.get_game(self, self.prev_i, self.prev_j).winner == 0:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            while not super(BaseAI, self).play(i, j):
                i = random.randint(0, 2)
                j = random.randint(0, 2)
        else:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            while not super(BaseAI, self).play(i, j, row, col):
                i = random.randint(0, 2)
                j = random.randint(0, 2)
                row = random.randint(0, 2)
                col = random.randint(0, 2)
        return True
