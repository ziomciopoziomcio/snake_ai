import numpy as np
import random
from main import Game, ai_move


class SnakeEnv:
    def __init__(self):
        self.game = Game()
        self.reset()

    def reset(self):
        self.game = Game()
        self.done = False
        return self._get_state()

    def _get_state(self):
        state = np.zeros((self.game.board_width, self.game.board_height))
        for x, y in self.game.snakes[0].positions:
            state[x, y] = 1
        state[self.game.food[0][0], self.game.food[0][1]] = 2
        return state

