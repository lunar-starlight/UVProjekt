from django.db import models

from typing import Optional


class Game(models.Model):
    # field = models.CharField(default='0'*9, max_length=9)
    player = 1
    winner = 0
    field = [0,0,0,0,0,0,0,0,0]

    def get_position(self, i: int, j: int) -> Optional[int]:
        if i < 0 or j < 0 or i > 2 or j > 2:
            return None
        return 3*i + j

    def toggle_player(self) -> None:
        self.player = 3 - self.player
    
    def check_win(self, i: int, j: int) -> bool:
        if self.field[j] == self.field[3 + j] == self.field[6 + j] or self.field[3*i] == self.field[3*i + 1] == self.field[3*i + 2]:
            return True
        if i == j:
            if self.field[0] == self.field[4] == self.field[8]:
                return True
        if i == 2-j:
            if self.field[2] == self.field[4] == self.field[6]:
                return True

    def place(self, p: int) -> bool:
        if self.field[p] == 0:
            self.field[p] = self.player
            return True
        else:
            return False

    def move(self, i: int, j: int) -> bool:
        p = self.get_position(i, j)
        if p is None or not self.place(p):
            return False
        if self.check_win(i, j):
            self.winner = self.player
        self.toggle_player()