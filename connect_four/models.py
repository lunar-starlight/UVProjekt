from typing import Optional

from django.conf import settings
from django.db import models

WIDTH = 7
HEIGHT = 6


class GameCF(models.Model):
    player = models.IntegerField(default=1)
    winner = models.IntegerField(default=0)
    p1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cf_p1', on_delete=models.DO_NOTHING, default=0, null=True)
    p2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cf_p2', on_delete=models.DO_NOTHING, default=0, null=True)
    game_over = models.BooleanField(default=False)

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
        dirs = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        field = [[None for j in range(WIDTH)] for i in range(HEIGHT)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = e.data

        def clamp(i, j):
            if i < 0 or j < 0:
                return (None, None)
            if i >= HEIGHT or j >= WIDTH:
                return (None, None)
            return (i, j)

        for d in dirs:
            for k1 in range(-3, 1):
                data = field[i][j]
                for k2 in range(k1, k1+4):
                    ii, jj = clamp(i + d[0]*k2, j + d[1]*k2)
                    if ii is None or data != field[ii][jj]:  # OOB or not a run
                        data = None
                        break
                if data is not None:
                    return True
        return False

    def place(self, i: int, j: int) -> bool:
        if self.get_data(i, j) is None:
            self.set_data(i, j, self.player)
            return True
        else:
            return False

    def play(self, col: int) -> bool:
        cells = DataCell.objects.filter(id_game=self.pk, col=col)
        row = HEIGHT
        for cell in cells:
            row = min(row, cell.row)
        row -= 1  # place above the highest piece
        print(f"Play at ({row}, {col})")
        if not self.place(row, col):
            print(f"ERR: Failed to place at ({row}, {col}).")
            return False
        if self.check_win(row, col):
            print(f"Game won. {self.player} won.")
            self.game_over = True
            self.winner = self.player
            if self.winner == 1:
                self.p1.won()
                self.p2.lost()
            if self.winner == 2:
                self.p1.lost()
                self.p2.won()
        if DataCell.objects.filter(id_game=self.pk).count() == WIDTH * HEIGHT:
            self.game_over = True
        self.toggle_player()
        return True

    def field(self):
        conv = {1: 'X', 2: 'O'}
        field = [['' for j in range(WIDTH)] for i in range(HEIGHT)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = conv[e.data]
        return field


class DataCell(models.Model):
    id_game = models.ForeignKey(GameCF, on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    data = models.IntegerField(default=0)
