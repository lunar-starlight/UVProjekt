from common.models import DataCell, Game
from common.templatetags.tags import icon


class GameCF(Game):
    WIDTH = 7
    HEIGHT = 6

    def check_win(self, i: int, j: int) -> bool:
        dirs = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        field = [[None for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = e.data

        def clamp(i, j):
            if i < 0 or j < 0:
                return (None, None)
            if i >= self.HEIGHT or j >= self.WIDTH:
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

    def play(self, col: int) -> bool:
        cells = DataCell.objects.filter(id_game=self.pk, col=col)
        row = self.HEIGHT
        for cell in cells:
            row = min(row, cell.row)
        row -= 1  # place above the highest piece
        super().play(row, col)
        return '', '', row, col

    def field(self):
        conv = {1: icon('clear', 'round'), 2: icon('fiber_manual_record', 'outlined')}
        field = [['' for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        for e in DataCell.objects.filter(id_game=self.pk):
            field[e.row][e.col] = conv[e.data]
        return field
