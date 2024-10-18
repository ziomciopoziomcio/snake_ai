import json
import os

import numpy as np

from main import run
import time

board_width = 20
board_height = 20
snake_speed = 100000
amount_of_food = 1
snake_amount = 1
score_type = 1
game_mode = 5
window_width = 800
window_height = 800
turned_on = False

qvalues = {}
counter = 0


def load():
    file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    qvalues_str_keys = data.get('qvalues', {})
    qvalues = {eval(k): np.array(v) for k, v in qvalues_str_keys.items()}
    counter = data.get('counter', 0) + 1
    return qvalues, counter


for j in range(1):
    qvalues, counter = load()
    for z in range(10):
        for i in range(100):
            qvalues, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width,
                                   window_height,
                                   score_type,
                                   game_mode, qvalues=qvalues, counter=counter, agent="on", visualise=False,
                                   exploration_rate=0.1)
