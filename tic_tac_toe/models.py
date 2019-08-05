from typing import Optional

from django.conf import settings
from django.db import models


class GameTTT(models.Model):
    player = models.IntegerField(default=1)
    winner = models.IntegerField(default=0)
    p1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ttt_p1', on_delete=models.DO_NOTHING, default=0, null=True)
    p2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ttt_p2', on_delete=models.DO_NOTHING, default=0, null=True)
    keep_score = models.BooleanField(default=True)
    game_over = models.BooleanField(default=False)
    play_id = models.IntegerField(default=0)
    play_url = models.CharField(default='ttt:play', max_length=100)

    def get_data(self, i: int, j: int) -> Optional[int]:
        try:
            d = DataCell.objects.get(id_game=self.id, row=i, col=j)
            return d.data
        except models.ObjectDoesNotExist:
            print("does not exist")
            return None

    def set_data(self, i: int, j: int, data: int):
        cell: DataCell
        try:
            cell = DataCell.objects.get(id_game=self.id, row=i, col=j)
            print(f"Modified cell at ({i}, {j}) with {data}.")
        except models.ObjectDoesNotExist:
            cell = DataCell(id_game=self, row=i, col=j)
            print(f"Added cell at ({i}, {j}) with {data}.")
        cell.data = data
        cell.save()

    def toggle_player(self) -> None:
        self.player = 3 - self.player
        self.save()

    def check_win(self, i: int, j: int) -> bool:
        if self.get_data(0, j) == self.get_data(1, j) == self.get_data(2, j) or self.get_data(i, 0) == self.get_data(i, 1) == self.get_data(i, 2):
            return True
        if i == j:
            if self.get_data(0, 0) == self.get_data(1, 1) == self.get_data(2, 2):
                return True
        if i == 2-j:
            if self.get_data(0, 2) == self.get_data(1, 1) == self.get_data(2, 0):
                return True
        return False

    def place(self, i: int, j: int, player: str = None) -> bool:
        if player is None:
            player = self.player
        if self.get_data(i, j) is None:
            self.set_data(i, j, player)
            return True
        else:
            # print(f"ERR: {self.get_data(i, j) is None}")
            return False

    def play(self, i: int, j: int, player: int = None) -> bool:
        print(f"Play at ({i}, {j})")
        if player is None:
            player = self.player
        if not self.place(i, j, player=player):
            print(f"ERR: Failed to place at ({i}, {j}) as player {player}.")
            return False
        if self.check_win(i, j):
            print(f"Game won. {player} won.")
            self.game_over = True
            self.winner = player
            # remove score keeping from here
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
        if DataCell.objects.filter(id_game=self.pk).count() == 9:
            self.game_over = True
        self.toggle_player()
        return True

    def field(self):
        conv = {1: 'X', 2: 'O'}
        field = [['' for j in range(3)] for i in range(3)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = conv[e.data]
        return field


class DataCell(models.Model):
    id_game = models.ForeignKey(GameTTT, on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    data = models.IntegerField(default=0)
