import random

from .models import GameTTT


class BaseAI(GameTTT):

    class Meta:
        proxy = True

    def play(self, i: int, j: int, player: int = None) -> bool:
        if super().play(i, j, player):
            if self.game_over:
                return True
            else:
                return self.move()
        else:
            return False


class RandomTTTAI(BaseAI):
    slug = 'random'

    class Meta:
        proxy = True

    def move(self):
        i = random.randint(0, self.WIDTH-1)
        j = random.randint(0, self.HEIGHT-1)
        while not super(BaseAI, self).play(i, j):
            i = random.randint(0, self.WIDTH-1)
            j = random.randint(0, self.HEIGHT-1)
        return True


class MinimaxTTTAI(BaseAI):
    slug = 'minimax'
    player = 2  # TODO: get actual palyer number
    SCORE = 100

    class Meta:
        proxy = True

    def get_available_moves(self, state):
        moves = list()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if state[i][j] is None:
                    moves.append((i, j))
        return moves

    def move(self):
        state = super(GameTTT, self).field()
        i, j = self.minimax(state, self.player)
        super(GameTTT, self).play(i, j)

    def minimax(self, state, player):
        moves = self.get_available_moves(state)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = [list(state[i]) for i in range(3)]
            clone[move[0]][move[1]] = player
            score = self.min_play(clone, 3-player)
            if score > best_score:
                best_move = move
                best_score = score
            print(f'move: ({move[0]}, {move[1]}), score: {score}')
        return best_move

    def min_play(self, state: list, player, depth=0):
        moves = self.get_available_moves(state)
        score = self.evaluate(state, depth)
        if not moves or score:
            return score
        best_score = float('inf')
        for move in moves:
            clone = [list(state[i]) for i in range(3)]
            clone[move[0]][move[1]] = player
            score = self.max_play(clone, 3-player, depth=depth+1)
            # print(f'\tmove: ({move[0]}, {move[1]}), score: {score}')
            if score < best_score:
                best_score = score
        return best_score

    def max_play(self, state: list, player, depth=0):
        moves = self.get_available_moves(state)
        score = self.evaluate(state, depth)
        if not moves or score:
            return score
        best_score = float('-inf')
        for move in moves:
            clone = [list(state[i]) for i in range(3)]
            clone[move[0]][move[1]] = player
            score = self.min_play(clone, 3-player, depth=depth+1)
            if score > best_score:
                best_score = score
        return best_score

    def evaluate(self, state: list, depth):
        if state[0][0] == state[1][1] == state[2][2]:
            if state[1][1] == self.player:
                return (self.SCORE - depth)
            elif state[1][1] is not None:
                return -(self.SCORE - depth)
        if state[0][2] == state[1][1] == state[2][0]:
            if state[1][1] == self.player:
                return (self.SCORE - depth)
            elif state[1][1] is not None:
                return -(self.SCORE - depth)

        for i in range(3):
            if state[i][0] == state[i][1] == state[i][2]:
                if state[i][1] == self.player:
                    return (self.SCORE - depth)
                elif state[i][1] is not None:
                    return -(self.SCORE - depth)
            if state[0][i] == state[1][i] == state[2][i]:
                if state[1][i] == self.player:
                    return (self.SCORE - depth)
                elif state[1][i] is not None:
                    return -(self.SCORE - depth)
        return 0


class NegamaxTTTAI(BaseAI):
    slug = 'negamax'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def get_available_moves(self, state):
        moves = list()
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if state[i][j] is None:
                    moves.append((i, j))
        return moves

    def move(self):
        state = super(GameTTT, self).field()
        i, j = (self.negamax(state, self.player, 10)[0])
        super(BaseAI, self).play(i, j)

    def negamax(self, state: list, player: int, depth: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves(state)
        score = self.evaluate(state, depth)
        if not moves or score or not depth:
            return ((-1, -1), colour * score)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = [list(state[i]) for i in range(3)]
            clone[move[0]][move[1]] = player
            score = -self.negamax(clone, 3-player, depth-1)[1]
            if score > best_score:
                best_move = move
                best_score = score
            # print(f'move: ({move[0]}, {move[1]}), score: {score}')
        return best_move, best_score

    def evaluate(self, state: list, depth: int):
        if state[0][0] == state[1][1] == state[2][2]:
            if state[1][1] == self.player:
                return depth
            elif state[1][1] is not None:
                return -depth
        if state[0][2] == state[1][1] == state[2][0]:
            if state[1][1] == self.player:
                return depth
            elif state[1][1] is not None:
                return -depth

        for i in range(3):
            if state[i][0] == state[i][1] == state[i][2]:
                if state[i][1] == self.player:
                    return depth
                elif state[i][1] is not None:
                    return -depth
            if state[0][i] == state[1][i] == state[2][i]:
                if state[1][i] == self.player:
                    return depth
                elif state[1][i] is not None:
                    return -depth
        return 0
