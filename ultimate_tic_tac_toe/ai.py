import random

from .models import GameUTTT


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
        row = self.prev_i
        col = self.prev_j
        if not self.is_free_pick():
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
        return i, j, row, col
