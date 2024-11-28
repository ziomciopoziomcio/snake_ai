import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import keras
import numpy as np

from main import run
import time


acceleration_mode = input("Acceleration mode? ONLY WITH NVIDIA GPU (y/n): ")
if acceleration_mode == "y":
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    # tf.debugging.set_log_device_placement(True)
    if physical_devices:
        print("GPU detected")
        for device in physical_devices:
            print(device)
    else:
        print("No GPU detected")
        exit()
    global qnetwork_glob


    @tf.function
    def run_with_tf(board_width, board_height, snake_speed, amount_of_food, snake_amount,
                    window_width, window_height, score_type, game_mode, qnetwork, counter):
        qnetwork_glob_pom, counter_loc = run(board_width, board_height, snake_speed, amount_of_food, snake_amount,
                   window_width, window_height, score_type, game_mode, qnetwork=qnetwork, counter=counter,
                   agent="on", visualise=False, exploration_rate=0.1, acceleration=True)
        global qnetwork_glob
        qnetwork_glob = qnetwork_glob_pom
        global counter_glob
        counter_glob = counter_loc

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
endless = False

if int(input("For endless mode press 1")) == 1:
    endless = True
else:
    print("endless mode off")

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

if endless == False:
    start_time = time.time()
    qnetwork, counter = load()
    if acceleration_mode == "y":
        qnetwork_glob = qnetwork
        counter_glob = counter
        with tf.device('/GPU:0'):
            for j in range(4):
                for z in range(10):
                    for i in range(20):
                        run_with_tf(board_width, board_height, snake_speed, amount_of_food,
                                                        snake_amount,
                                                        window_width, window_height, score_type, game_mode,
                                                        qnetwork=qnetwork_glob,
                                                        counter=counter_glob)
                        # qnetwork, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount,
                        #                         window_width, window_height, score_type, game_mode, qnetwork=qnetwork,
                        #                         counter=counter, agent="on", visualise=False, exploration_rate=0.1)
        qnetwork = qnetwork_glob
        counter = counter_glob
    else:
        for j in range(1):
            for z in range(300):
                for i in range(10):
                    qnetwork, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width,
                                            window_height,
                                            score_type,
                                            game_mode, qnetwork=qnetwork, counter=counter, agent="on", visualise=False,
                                            exploration_rate=0.1)

if endless:
    qnetwork, counter = load()
    while True:
        for x in range(1000):
            qnetwork, counter = run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width,
                                    window_height,
                                    score_type,
                                    game_mode, qnetwork=qnetwork, counter=counter, agent="on", visualise=False,
                                    exploration_rate=0.1)
        save(qnetwork, counter)


save(qnetwork, counter)
end_time = time.time()
print("Time taken: ", end_time - start_time)

# if acceleration_mode == "y":
#     print("GPU usage details:")
#     print(tf.config.experimental.get_memory_info('GPU:0'))
