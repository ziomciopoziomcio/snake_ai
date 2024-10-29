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


def load():
    file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    qvalues_str_keys = data.get('qvalues', {})
    qvalues = {eval(k): np.array(v) for k, v in qvalues_str_keys.items()}
    counter = data.get('counter', 0) + 1
    return qvalues, counter


def save(qvalues_save, counter_save):
    file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
    qvalues_str_keys = {str(k): v.tolist() for k, v in qvalues_save.items()}
    data = {
        'qvalues': qvalues_str_keys,
        'counter': counter_save
    }
    with open(file_path, 'w') as f:
        json.dump(data, f)


start_time = time.time()
qvalues, counter = load()

for j in range(5):
    for z in range(50):
        for i in range(100):
            qvalues, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width,
                                   window_height,
                                   score_type,
                                   game_mode, qvalues=qvalues, counter=counter, agent="on", visualise=False,
                                   exploration_rate=0.1)
save(qvalues, counter)
end_time = time.time()
print("Time taken: ", end_time - start_time)
