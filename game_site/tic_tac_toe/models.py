from django.db import models
from django.urls import reverse
from typing import Optional

class Player(models.Model):
    name = models.CharField(max_length=50)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('ttt:create_user')

class GameTTT(models.Model):
    field = models.CharField(default='0'*9, max_length=9)
    player = models.IntegerField(default=1)
    winner = models.IntegerField(default=0)
    p1 = models.ForeignKey(Player, related_name='ttt_p1', on_delete=models.DO_NOTHING, default=0)
    p2 = models.ForeignKey(Player, related_name='ttt_p2', on_delete=models.DO_NOTHING, default=0)
    keep_score = models.BooleanField(default=True)
    game_over = models.BooleanField(default=False)
    play_id = models.IntegerField(default=0)
    play_url = models.CharField(default='ttt:play', max_length=100)

    def get_position(self, i: int, j: int) -> Optional[int]:
        if i < 0 or j < 0 or i > 2 or j > 2:
            return None
        return 3*i + j

    def toggle_player(self) -> None:
        self.player = 3 - self.player
        self.save()
    
    def check_win(self, i: int, j: int) -> bool:
        if self.field[j] == self.field[3 + j] == self.field[6 + j] or self.field[3*i] == self.field[3*i + 1] == self.field[3*i + 2]:
            return True
        if i == j:
            if self.field[0] == self.field[4] == self.field[8]:
                return True
        if i == 2-j:
            if self.field[2] == self.field[4] == self.field[6]:
                return True

    def place(self, p: int, player: str = None) -> bool:
        if player is None:
            player = self.player
        if self.field[p] == '0':
            self.field = self.field[:p] + str(player) + self.field[p+1:]
            return True
        else:
            return False

    def play(self, _, i: int, j: int, player: int = None) -> bool:
        if player is None:
            player = self.player
        p = self.get_position(i, j)
        if p is None or not self.place(p, player=player):
            return False
        if self.check_win(i, j):
            self.game_over = True
            self.winner = player
            if self.keep_score and self.winner == 1:
                self.p1.wins += 1
                self.p2.losses += 1
                self.p1.save()
                self.p2.save()
            if self.keep_score and self.winner == 2:
                self.p1.losses += 1
                self.p2.wins += 1
                self.p1.save()
                self.p2.save()
        if self.field.count('0') == 0:
            self.game_over = True
        self.toggle_player()
        self.save()
        return True

    def context(self):
        conv = {'0': ' ', '1': 'X', '2': 'O'}
        context = {'field'+str(i): conv[self.field[i]] for i in range(9)}
        context['winner'] = conv[str(self.winner)]
        return context
