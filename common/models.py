from typing import Optional

from django.conf import settings
from django.db import models

from polymorphic.models import PolymorphicModel


class Game(PolymorphicModel):
    player = models.IntegerField(default=1)
    winner = models.IntegerField(default=0)
    p1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_p1", on_delete=models.DO_NOTHING, default=0, null=True)
    p2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_p2", on_delete=models.DO_NOTHING, default=0, null=True)
    game_over = models.BooleanField(default=False)

    WIDTH = 0
    HEIGHT = 0

    @classmethod
    def new_game(cls, p1, p2):
        g = cls(p1=p1, p2=p2)
        g.save()
        return g

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

    def current_player(self):
        if self.player == 1:
            return self.p1
        else:
            return self.p2

    def check_win(self, i: int, j: int) -> bool:
        pass

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
            if self.winner == 1:
                self.p1.won()
                self.p2.lost()
            if self.winner == 2:
                self.p1.lost()
                self.p2.won()
        if DataCell.objects.filter(id_game=self.pk).count() == self.WIDTH * self.HEIGHT:
            self.game_over = True
        self.toggle_player()
        self.save()
        return True

    def field(self):
        field = [[None for j in range(3)] for i in range(3)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = e.data
        return field


class DataCell(models.Model):
    id_game = models.ForeignKey('Game', on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    data = models.IntegerField(default=0)
