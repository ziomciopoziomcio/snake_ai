import numpy as np
import random
from main import Game, ai_move

head_position = None
points = None

def update_points(p):
    global points
    points = p

def update_head_position(position):
    global head_position
    head_position = position

class SnakeEnv:
    def __init__(self):
        self.game = Game()
        self.reset()

    def reset(self):
        self.game = Game()
        self.done = False
        return self._get_state()



