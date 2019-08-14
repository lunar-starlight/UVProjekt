import random

from .models import GameCF


class BaseAI(GameCF):
    column_row = [5]*7

    class Meta:
        proxy = True

    def play(self, col: int) -> bool:
        if super().play(col):
            self.column_row[col] -= 1
            if self.game_over:
                return True
            else:
                return self.move()
        else:
            return False

    def get_available_moves(self):
        moves = list()
        for col in [3, 2, 4, 1, 5, 0, 6]:
            if self.column_row[col] >= 0:
                moves.append(col)
        return moves

    def evaluate(self, state: list, depth: int):
        # horizontal check
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH - 3):
                if state[i][j+0] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                    if state[i][j] == self.player:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # vertical check
        for i in range(self.HEIGHT - 3):
            for j in range(self.WIDTH):
                if state[i+0][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                    if state[i][j] == self.player:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # diagonal 1 check
        for i in range(self.HEIGHT - 3):
            for j in range(self.WIDTH - 3):
                if state[i+0][j+0] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    if state[i][j] == self.player:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # diagonal 2 check
        for i in range(self.HEIGHT - 3):
            for j in range(3, self.WIDTH):
                if state[i+0][j-0] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    if state[i][j] == self.player:
                        return depth
                    elif state[i][j] is not None:
                        return -depth
        return 0


class RandomCFAI(BaseAI):
    slug = 'random'

    class Meta:
        proxy = True

    def move(self):
        col = random.randint(0, self.WIDTH-1)
        while not super(BaseAI, self).play(col):
            col = random.randint(0, self.WIDTH-1)
        return True


class NegamaxTTTAI(BaseAI):
    slug = 'negamax'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player, 6)[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves()
        score = self.evaluate(state, depth)
        if not moves or score or not depth:
            return (-1, colour * score)
        best_move = moves[0]
        best_score = float('-inf')
        for col in moves:
            clone = [list(state[i]) for i in range(self.HEIGHT)]

            row = self.HEIGHT
            for i in range(self.HEIGHT):
                if clone[i][col] is not None:
                    row = i
                    break
            row -= 1  # place above the highest piece

            clone[row][col] = player
            score = -self.negamax(clone, 3-player, depth-1)[1]
            if score > best_score:
                best_move = col
                best_score = score
            # if depth > 4:
            #     print('\t'*(6-depth)+f'move: ({col}), score: {score}')
        return best_move, best_score


class NegamaxPrunningTTTAI(BaseAI):
    slug = 'negamax-prunning'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player, 10, float('-inf'), float('inf'))[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves()
        score = self.evaluate(state, depth)
        if not moves or score or not depth:
            return (-1, colour * score)
        best_move = moves[0]
        best_score = float('-inf')
        for col in moves:
            clone = [list(state[i]) for i in range(self.HEIGHT)]

            row = self.HEIGHT
            for i in range(self.HEIGHT):
                if clone[i][col] is not None:
                    row = i
                    break
            row -= 1  # place above the highest piece

            clone[row][col] = player
            score = -self.negamax(clone, 3-player, depth-1, -beta, -alpha)[1]
            if score > best_score:
                best_move = col
                best_score = score
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
            # if depth > 4:
            #     print('\t'*(6-depth)+f'move: ({col}), score: {score}')
        return best_move, best_score


class PrincipalVariationSearchAI(BaseAI):
    slug = 'pvs'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.pvs(state, self.player, 10, float('-inf'), float('inf'))[0]
        super(BaseAI, self).play(col)

    def pvs(self, state: list, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves()
        score = self.evaluate(state, depth)
        if not moves or score or not depth:
            return (-1, colour * score)
        best_move = moves[0]
        best_score = float('-inf')
        for col in moves:
            clone = [list(state[i]) for i in range(self.HEIGHT)]

            row = self.HEIGHT
            for i in range(self.HEIGHT):
                if clone[i][col] is not None:
                    row = i
                    break
            row -= 1  # place above the highest piece

            clone[row][col] = player
            if col == moves[0]:
                score = -self.pvs(clone, 3-player, depth-1, -beta, -alpha)[1]
            else:
                score = -self.pvs(clone, 3-player, depth-1, -alpha-1, -alpha)[1]
                if alpha < score < beta and depth > 2:
                    score = -self.pvs(clone, 3-player, depth-1, -beta, -score)[1]
            if score > best_score:
                best_move = col
                best_score = score
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
            # if depth > 4:
            #     print('\t'*(6-depth)+f'move: ({col}), score: {score}')
        return best_move, best_score


rand_table = [[(random.randint(0, 2**16), random.randint(0, 2**32))
               for j in range(7)] for i in range(6)]
table = dict()


class NegimaxABTablesAI(BaseAI):
    slug = 'negamax-tables'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def move(self):
        self.state = super(GameCF, self).field()
        self.state_hash = self.hash(self.state)
        for col in range(self.WIDTH):
            row = self.HEIGHT
            for i in range(self.HEIGHT):
                if self.state[i][col] is not None:
                    row = i
                    break
            self.column_row[col] = row-1
        col = self.negamax(self.player, 10, float('-inf'), float('inf'))[0]
        return super(BaseAI, self).play(col)

    class TT:

        def __init__(self, val=None, d=None, flag=None):
            self.value = val
            self.depth = d
            self.flag = flag

    def hash(self, state: list) -> int:
        hash = 0
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if state[i][j] is not None:
                    hash ^= rand_table[i][j][state[i][j]-1]
        return hash

    def tt_lookup(self, state_hash: int):
        return table.get(state_hash, self.TT())

    def tt_store(self, state_hash: int, tt_entry: TT):
        table[state_hash] = tt_entry

    def negamax(self, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player - 3)
        alpha_orig = alpha
        if depth > 9:
            print(self.column_row)

        tt_entry: self.TT = self.tt_lookup(self.state_hash)
        if tt_entry.value is not None and tt_entry.depth >= depth:
            if tt_entry.flag == 'EXACT':
                return (tt_entry.move, tt_entry.value)
            elif tt_entry.flag == 'LOWERBOUND':
                alpha = max(alpha, tt_entry.value)
            elif tt_entry.flag == 'UPPERBOUND':
                beta = min(beta, tt_entry.value)
            if alpha >= beta:
                return (tt_entry.move, tt_entry.value)

        moves = self.get_available_moves()
        score = self.evaluate(self.state, depth)
        if not moves or score or not depth:
            return (-1, colour * score)
        best_move = moves[0]
        best_score = float('-inf')
        for col in moves:
            row = self.column_row[col]
            self.column_row[col] -= 1

            self.state[row][col] = player
            self.state_hash ^= rand_table[row][col][player-1]
            score = -self.negamax(3-player, depth-1, -beta, -alpha)[1]
            if score > best_score:
                best_move = col
                best_score = score
            alpha = max(alpha, best_score)
            self.state[row][col] = None
            self.state_hash ^= rand_table[row][col][player-1]
            self.column_row[col] += 1
            if alpha >= beta:
                break

        tt_entry.value = best_score
        tt_entry.move = best_move
        tt_entry.depth = depth
        if best_score <= alpha_orig:
            tt_entry.flag = 'UPPERBOUND'
        elif best_score >= beta:
            tt_entry.flag = 'LOWERBOUND'
        else:
            tt_entry.flag = 'EXACT'

        self.tt_store(self.state_hash, tt_entry)
        return best_move, best_score
