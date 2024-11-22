import json
import os

import keras
import numpy as np

from main import run
import time

board_width = 20
board_height = 20
snake_speed = 100000
amount_of_food = 1
snake_amount = 1
score_type = 1
game_mode = 6
window_width = 800
window_height = 800
turned_on = False


# def load():
#     file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
#     with open(file_path, 'r') as f:
#         data = json.load(f)
#     qvalues_str_keys = data.get('qvalues', {})
#     qvalues = {eval(k): np.array(v) for k, v in qvalues_str_keys.items()}
#     counter = data.get('counter', 0) + 1
#     return qvalues, counter
#
#
# def save(qvalues_save, counter_save):
#     file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
#     qvalues_str_keys = {str(k): v.tolist() for k, v in qvalues_save.items()}
#     data = {
#         'qvalues': qvalues_str_keys,
#         'counter': counter_save
#     }
#     with open(file_path, 'w') as f:
#         json.dump(data, f)


def load():
    file_path = os.path.join(os.path.dirname(__file__), 'deepqnetwork.h5')
    with open(file_path, 'r') as f:
        qnetwork = keras.Sequential()
        qnetwork.add(keras.layers.Dense(24, input_shape=(20 * 20,), activation='relu'))
        qnetwork.add(keras.layers.Dense(24, activation='relu'))
        qnetwork.add(keras.layers.Dense(4, activation='linear'))
        qnetwork.compile(optimizer='adam', loss='mse')
        qnetwork.load_weights(file_path)
    qnetwork = qnetwork
    file_path = os.path.join(os.path.dirname(__file__), 'deepqnetworkcounter.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    counter = data.get('counter', 0)
    return qnetwork, counter


def save(qnetwork_save, counter_save):
    file_path = os.path.join(os.path.dirname(__file__), 'deepqnetwork.h5')
    qnetwork_save.save(file_path)
    file_path = os.path.join(os.path.dirname(__file__), 'deepqnetworkcounter.json')
    with open(file_path, 'w') as f:
        json.dump({'counter': counter_save}, f)


start_time = time.time()
qnetwork, counter = load()

for j in range(20):
    for z in range(1):
        for i in range(1):
            qnetwork, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width,
                                    window_height,
                                    score_type,
                                    game_mode, qnetwork=qnetwork, counter=counter, agent="on", visualise=False,
                                    exploration_rate=0.1)
save(qnetwork, counter)
end_time = time.time()
print("Time taken: ", end_time - start_time)
