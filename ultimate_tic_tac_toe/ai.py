import random
from itertools import product
from random import shuffle

from common.models import Game

from .models import GameUTTT

eval_t = dict()


class BaseAI(GameUTTT):

    class Meta:
        proxy = True

    def play(self, i: int, j: int, row: int = None, col: int = None) -> bool:
        if super().current_player().username != 'ai':
            super().play(i, j, row, col)
        self.player_num = self.player
        self.row = self.prev_i
        self.col = self.prev_j
        if self.game_over:
            return True
        else:
            self.state = self.game_list()
            self.dbg = False
            self.glob = [[None for _ in range(3)] for _ in range(3)]
            for row in range(3):
                for col in range(3):
                    if self.state[row][col] is None:
                        self.state[row][col] = [[None for _ in range(3)] for _ in range(3)]
                    else:
                        if self.state[row][col].winner:
                            self.glob[row][col] = self.state[row][col].winner
                        elif self.state[row][col].game_over:
                            self.glob[row][col] = 3  # tie
                        self.state[row][col] = Game.field(self.state[row][col])
            return self.move()

    def ttt_eval(self, state, player):
        """special values:
        100: win
        101: full & draw
        102: no win possible
        """
        res = 0
        d = True
        # horizontal
        for row in range(3):
            cptH = 0
            for col in range(3):
                if state[row][col] == player:
                    cptH += 1
                elif state[row][col] is not None:
                    cptH = -1
                    break
            if cptH == 3:
                return 100
            elif cptH == 2:
                res += 7
            elif cptH == 1:
                res += 2
            if cptH >= 0:
                d = False

        # vertical
        for col in range(3):
            cptV = 0
            for row in range(3):
                if state[row][col] == player:
                    cptV += 1
                elif state[row][col] is not None:
                    cptV = -1
                    break
            if cptV == 3:
                return 100
            elif cptV == 2:
                res += 7
            elif cptV == 1:
                res += 2
            if cptV >= 0:
                d = False

        # diag 1
        cptD1 = 0
        for k in range(3):
            if state[k][k] == player:
                cptD1 += 1
            elif state[k][k] is not None:
                cptD1 = -1
                break
        if cptD1 == 3:
            return 100
        elif cptD1 == 2:
            res += 7
        elif cptD1 == 1:
            res += 2
        if cptD1 >= 0:
            d = False

        # diag 2
        cptD2 = 0
        for k in range(3):
            if state[k][2-k] == player:
                cptD2 += 1
            elif state[k][2-k] is not None:
                cptD2 = -1
                break
        if cptD2 == 3:
            return 100
        elif cptD2 == 2:
            res += 7
        elif cptD2 == 1:
            res += 2
        if cptD2 >= 0:
            d = False

        f = True
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    f = False
        if f:
            return 101
        if d:
            return 102
        return res


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


class NegamaxABAI(BaseAI):
    slug = 'negamax-ab'

    class Meta:
        proxy = True

    def move(self):
        self.max_depth = 7
        move = self.negamax(self.player_num, self.max_depth, float('-inf'), float('inf'))[0]
        print(move)
        super(BaseAI, self).play(*move)
        return move

    def get_available_moves(self):
        moves = list()
        moves2 = list()
        if self.glob[self.row][self.col] is not None:
            for i, j, row, col in product(range(3), repeat=4):
                if self.glob[row][col] is None:
                    if self.state[row][col][i][j] is None:
                        if self.glob[i][j] is None:
                            moves.append((i, j, row, col))
                        else:
                            moves2.append((i, j, row, col))
        else:
            for i, j in product(range(3), repeat=2):
                if self.state[self.row][self.col][i][j] is None:
                    if self.glob[i][j] is None:
                        moves.append((i, j, self.row, self.col))
                    else:
                        moves2.append((i, j, self.row, self.col))
        if len(moves) + len(moves2) > 15:
            shuffle(moves)
            shuffle(moves2)
            moves.extend(moves2)
            return moves
        else:
            # if self.dbg:
            #     print(moves2)
            #     print(self.glob[i][j] is None)
            moves.extend(moves2)
            return moves

    def get_ttt_board_n(self, state):
        n = 0
        for i in range(3):
            for j in range(3):
                n <<= 2
                if state[i][j] is not None:
                    n |= (state[i][j] & 0x3)
        return n

    def make_move(self, move, player):
        i, j, row, col = move
        self.state[row][col][i][j] = player
        code = self.ttt_eval_t(self.state[row][col]) & 0x7
        if code == 4:
            self.glob[row][col] = 1
        elif code == 5:
            self.glob[row][col] = 2
        elif code >= 3:
            self.glob[row][col] = 3
        self.row, self.col = i, j

    def unmake_move(self, move, prev_row, prev_col):
        i, j, row, col = move
        self.state[row][col][i][j] = None
        code = self.ttt_eval_t(self.state[row][col]) & 0x7
        if code == 4:
            self.glob[row][col] = 1
        elif code == 5:
            self.glob[row][col] = 2
        elif code >= 3:
            self.glob[row][col] = 3
        else:
            self.glob[row][col] = None
        self.row, self.col = prev_row, prev_col

    def ttt_eval_t(self, state):
        """codes:
        0: Nothing special
        1: p1 cannot win
        2: p2 cannot win
        3: Draw & not full
        4: p1 wins
        5: p2 wins
        6: Draw & full
        7: Double win (impossible)
        val: ai positive"""
        n = self.get_ttt_board_n(state)
        # print(state, n)
        if n not in eval_t:
            c1 = self.ttt_eval(state, 1)
            c2 = self.ttt_eval(state, 2)
            # if self.dbg:
            #     print(f'c1: {c1}, c2: {c2}')
            if c1 == c2 == 100:
                val = 0
                code = 7
            elif c1 == 100:
                val = 0
                code = 4
            elif c2 == 100:
                val = 0
                code = 5
            elif c1 == 101 or c2 == 101:
                val = 0
                code = 6
            elif c1 == c2 == 102:
                val = 0
                code = 3
            elif c1 == 102:
                val = (c2 - c1) * (2*self.player_num - 3)
                code = 1
            elif c2 == 102:
                val = (c2 - c1) * (2*self.player_num - 3)
                code = 2
            else:
                val = (c2 - c1) * (2*self.player_num - 3)
                code = 0
            eval_t[n] = (val << 3) + code
        # print(eval_t[n])
        return eval_t[n]

    def evaluate(self, player):
        """codes:
        1000000: ai wins
        -1000000: human wins
        0xffffff: draw
        val: ai positive
        """
        globP1 = [[None for _ in range(3)] for _ in range(3)]
        globP2 = [[None for _ in range(3)] for _ in range(3)]
        res = 0
        for row in range(3):
            for col in range(3):
                currEv = self.ttt_eval_t(self.state[row][col])
                val = currEv >> 3
                code = currEv & 0x7
                # if self.dbg:
                #     print(f'({row}, {col}) code: {code}, val: {val}')
                #     print('\t', self.state[row][col])
                if code == 0:
                    if row == col == 1:
                        res += 5 * val
                    elif row == 1 or col == 1:
                        res += val
                    else:
                        res += 3 * val
                elif code == 1:
                    globP1[row][col] = 3
                elif code == 2:
                    globP2[row][col] = 3
                elif code == 4:
                    globP1[row][col] = 1
                    globP2[row][col] = 1
                elif code == 5:
                    globP1[row][col] = 2
                    globP2[row][col] = 2
                else:
                    globP1[row][col] = 3
                    globP2[row][col] = 3
                # if 3 != globP1[row][col] != self.glob[row][col]:
                #     print(f'mismatch ({row}, {col}) code: {code}, val: {val}')
                #     print(f'should be {self.glob[row][col]}')
        globEvP1 = self.ttt_eval_t(globP1)
        globEvP2 = self.ttt_eval_t(globP2)
        # if self.dbg:
        #     print(globP1, globEvP1)
        #     print(globP2, globEvP2)
        if globEvP1 & 0x7 == 4:  # p1 wins
            return -(2*self.player_num - 3) * 1000000
        if globEvP2 & 0x7 == 5:  # p2 wins
            return (2*self.player_num - 3) * 1000000
        if globEvP1 & 0x7 >= 3:  # draw
            return 0xffffff
        if player == 1:
            return 5*(globEvP1 >> 3) + res
        else:
            return 5*(globEvP2 >> 3) + res

    def negamax(self, player: int, depth: int, alpha: int, beta: int):
        if self.max_depth - depth < 2:
            self.dbg = True
        else:
            self.dbg = False
        colour = (2*player - 3) * (2*self.player_num - 3)  # 1 if player is ai, -1 if player is human
        moves = self.get_available_moves()
        score = colour * self.evaluate(player)  # ai positive * {1, -1} = {ai+, ai-} = {ai+, h+} = pl+
        # if self.dbg:
        #     print(f'sc: {score} p: {player} d: {depth}')

        if abs(score) == 0xffffff:
            return (-1, -1, -1, -1), 0
        if abs(score) == 1000000:
            return (-1, -1, -1, -1), score
        if depth <= 0 or not moves:
            return (-1, -1, -1, -1), score

        best_move = moves[0]
        best_score = float('-inf')
        prev_row = self.row
        prev_col = self.col

        for move in moves:
            # if move == (1, 0, 2, 1) and depth == 5:
            #     self.dbg = True
            self.make_move(move, player)
            score = -self.negamax(3-player, depth-1, -beta, -alpha)[1]
            self.unmake_move(move, prev_row, prev_col)
            if self.dbg:
                print('\t'*(self.max_depth-depth) + f'move: {move}, score: {score}')
            # if move == (1, 0, 2, 1) and depth == 5:
            #     self.dbg = False
            if score > best_score:
                best_move = move
                best_score = score
                if score == 1000000:
                    break  # found winning move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        if self.max_depth - depth == 2:
            self.dbg = True
        return best_move, best_score
