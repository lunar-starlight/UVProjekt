import random

from .models import GameCF


class BaseAI(GameCF):
    column_row = [5]*7
    # player_num = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def play(self, col: int) -> bool:
        if super().current_player().username != 'ai':
            b = super().play(col)
            if b:
                self.column_row[col] -= 1
        self.player_num = self.player
        if self.game_over:
            return True
        else:
            return self.move()

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
                    if state[i][j] == self.player_num:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # vertical check
        for i in range(self.HEIGHT - 3):
            for j in range(self.WIDTH):
                if state[i+0][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                    if state[i][j] == self.player_num:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # diagonal 1 check
        for i in range(self.HEIGHT - 3):
            for j in range(self.WIDTH - 3):
                if state[i+0][j+0] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    if state[i][j] == self.player_num:
                        return depth
                    elif state[i][j] is not None:
                        return -depth

        # diagonal 2 check
        for i in range(self.HEIGHT - 3):
            for j in range(3, self.WIDTH):
                if state[i+0][j-0] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    if state[i][j] == self.player_num:
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

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player_num, 6)[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int):
        colour = (2*player - 3) * (2*self.player_num - 3)
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


class NegamaxPruningTTTAI(BaseAI):
    slug = 'negamax-pruning'

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player, 10, float('-inf'), float('inf'))[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player_num - 3)
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

    class Meta:
        proxy = True

    def move(self):
        state = super(GameCF, self).field()
        col = self.pvs(state, self.player_num, 10, float('-inf'), float('inf'))[0]
        super(BaseAI, self).play(col)

    def pvs(self, state: list, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player_num - 3)
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
                    score = -self.pvs(clone, 3-player, depth-1, -beta, -alpha)[1]
            if score > best_score:
                best_move = col
                best_score = score
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
            # if depth > 4:
            #     print('\t'*(6-depth)+f'move: ({col}), score: {score}')
        return best_move, best_score


rand_table = [[(random.randint(0, 2**32), random.randint(0, 2**32))
               for j in range(7)] for i in range(6)]
# table = [None] * (2**16)
table = dict()


class NegamaxABTablesAI(BaseAI):
    slug = 'negamax-tables'

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
        col = self.negamax(self.player_num, 12, float('-inf'), float('inf'))[0]
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
        # return table[state_hash] or self.TT()

    def tt_store(self, state_hash: int, tt_entry: TT):
        table[state_hash] = tt_entry

    def negamax(self, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player_num - 3)
        alpha_orig = alpha
        tt_entry: self.TT = self.tt_lookup(self.state_hash)
        if tt_entry.value is not None and tt_entry.depth >= depth - 2:
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


class MTDFAI(NegimaxABTablesAI):
    slug = 'mtd-f'

    class Meta:
        proxy = True

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
        col = self.MTD(self.player_num, 0, 11)[0]
        return super(BaseAI, self).play(col)

    def MTD(self, player, f, depth):
        g = f
        upperbound = float('+inf')
        lowerbound = float('-inf')
        move = -1
        while lowerbound < upperbound:
            beta = max(g, lowerbound+1)
            move, g = self.negamax(player, depth, beta-1, beta)
            if g < beta:
                upperbound = g
            else:
                lowerbound = g
        return move, g


class BNSAI(NegimaxABTablesAI):
    slug = 'bns'

    class Meta:
        proxy = True

    def get_available_moves(self):
        moves = list()
        for col in reversed([3, 2, 4, 1, 5, 0, 6]):
            if self.column_row[col] >= 0:
                moves.append(col)
        return moves

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
        col = self.BNS(20, -20, 20)
        return super(BaseAI, self).play(col)

    def BNS(self, depth, alpha: int, beta: int):
        moves = self.get_available_moves()
        subtree_count = len(moves)
        if moves:
            best_move = moves[0]
        while subtree_count != 1:
            test = self.next_guess(alpha, beta, subtree_count)
            better_count = 0
            for col in moves:
                row = self.column_row[col]
                self.column_row[col] -= 1
                self.state[row][col] = self.player_num
                self.state_hash ^= rand_table[row][col][self.player_num-1]
                score = -self.negamax(3-self.player_num, depth-int((1.5)*len(moves)), -test, -test+1)[1]
                self.state[row][col] = None
                self.state_hash ^= rand_table[row][col][self.player_num-1]
                self.column_row[col] += 1
                # print(f'move: ({col}), score: {score}')
                if score >= test:
                    best_move = col
                    better_count += 1
            if better_count != 0:
                subtree_count = better_count
                alpha = test
            else:
                beta = test
            if beta - alpha < 2:
                break
        return best_move

    def next_guess(self, alpha, beta, subtree_count):
        return alpha + (beta - alpha) * (subtree_count - 1) // (subtree_count)
