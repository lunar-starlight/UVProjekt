import random

from .models import GameCF


class BaseAI(GameCF):

    class Meta:
        proxy = True

    def play(self, col: int) -> bool:
        if super().play(col):
            if self.game_over:
                return True
            else:
                return self.move()
        else:
            return False


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

    def get_available_moves(self, state):
        moves = list()
        for col in range(self.WIDTH):
            if state[0][col] is None:
                moves.append(col)
        return moves

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player, 6)[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves(state)
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
            if depth > 4:
                print('\t'*(6-depth)+f'move: ({col}), score: {score}')
        return best_move, best_score

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


class NegamaxPrunningTTTAI(BaseAI):
    slug = 'negamax-prunning'
    player = 2  # TODO: get actual palyer number

    class Meta:
        proxy = True

    def get_available_moves(self, state):
        moves = list()
        for col in range(self.WIDTH):
            if state[0][col] is None:
                moves.append(col)
        return moves

    def move(self):
        state = super(GameCF, self).field()
        col = self.negamax(state, self.player, 10, float('-inf'), float('inf'))[0]
        super(BaseAI, self).play(col)

    def negamax(self, state: list, player: int, depth: int, alpha: int, beta: int):
        colour = (2*player - 3) * (2*self.player - 3)
        moves = self.get_available_moves(state)
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
