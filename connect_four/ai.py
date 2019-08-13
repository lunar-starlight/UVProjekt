import random

from .models import GameCF


class BaseAI(GameCF):

    class Meta:
        proxy = True

    def play(self, col: int) -> bool:
        if super().play(col):
            if self.game_over:
                return True
            else:
                return self.move()
        else:
            return False


class RandomCFAI(BaseAI):
    slug = 'random'

    class Meta:
        proxy = True

    def move(self):
        col = random.randint(0, self.WIDTH-1)
        while not super(BaseAI, self).play(col):
            col = random.randint(0, self.WIDTH-1)
        return True
