import numpy as np
import random
import json
import os
import keras
import tensorflow as tf


class SnakeEnv:
    def __init__(self, qnetwork, counter, width, height, agent="off", exploration_rate=0.1, acceleration_mode=False):
        if agent == "off":
            self.load()
            self.qnetwork = keras.Sequential()
            self.qnetwork.add(keras.layers.Dense(24, input_shape=(width * height,), activation='relu'))
            self.qnetwork.add(keras.layers.Dense(24, activation='relu'))
            self.qnetwork.add(keras.layers.Dense(4, activation='linear'))
            self.qnetwork.compile(optimizer='adam', loss='mse')
            self.counter = 0
        else:
            self.qnetwork = qnetwork
            self.counter = counter
        if acceleration_mode:
            self.mode = 1
        else:
            self.mode = 0
        self.learning_rate = 0.1
        self.discount = 0.9
        self.exploration_rate = exploration_rate

    def update(self, state, action, next_state, reward):
        if self.mode == 1:
            state = tf.convert_to_tensor([state], dtype=tf.float32)
            next_state = tf.convert_to_tensor([next_state], dtype=tf.float32)
            result = self.qnetwork(state)
            result_next = self.qnetwork(next_state)
            target = tf.identity(result)
            max_next_q = tf.reduce_max(result_next[0])
            updated_value = reward + self.discount * max_next_q
            target = tf.tensor_scatter_nd_update(
                target,
                indices=[[0, action]],
                updates=[target[0, action] + self.learning_rate * (updated_value - target[0, action])]
            )
            self.qnetwork.fit(state, target, epochs=1, verbose=0)
        else:
            state = np.array([state])
            next_state = np.array([next_state])
            result = self.qnetwork.predict(state, verbose=0)
            result_next = self.qnetwork.predict(next_state, verbose=0)
            result[0][action] = result[0][action] + self.learning_rate * (
                    reward + self.discount * max(result_next[0]) - result[0][action])
            self.qnetwork.fit(state, result, epochs=1, verbose=0)

    def get_action(self, state):
        if self.mode == 1:
            state = tf.convert_to_tensor([state], dtype=tf.float32)
        else:
            state = np.array([state])
        p = random.random()
        if p < self.exploration_rate:
            return random.randint(0, 3)
        else:
            # result = self.qnetwork.predict(state, verbose=0)
            # value = max(result)
            # index = random.choice([i for i, v in enumerate(result) if v == value])
            # return index
            if self.mode == 1:
                result = self.qnetwork(state)
                index = tf.argmax(result[0])
                return index
            else:
                result = self.qnetwork.predict(state, verbose=0)
                #print(result)
                index = np.argmax(result[0])  # Use np.argmax to find the index of the maximum value
                return index

    def save(self):
        file_path = os.path.join(os.path.dirname(__file__), 'deepqnetwork.h5')
        self.qnetwork.save(file_path)
        file_path = os.path.join(os.path.dirname(__file__), 'deepqnetworkcounter.json')
        with open(file_path, 'w') as f:
            json.dump({'counter': self.counter}, f)


    def load(self):
        file_path = os.path.join(os.path.dirname(__file__), 'deepqnetwork.h5')
        qnetwork = keras.Sequential()
        qnetwork.add(keras.layers.Dense(24, input_shape=(20 * 20,), activation='relu'))
        qnetwork.add(keras.layers.Dense(24, activation='relu'))
        qnetwork.add(keras.layers.Dense(4, activation='linear'))
        qnetwork.compile(optimizer='adam', loss='mse')
        qnetwork.load_weights(file_path)
        self.qnetwork = qnetwork
        file_path = os.path.join(os.path.dirname(__file__), 'deepqnetworkcounter.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.counter = data.get('counter', 0)


def generate_empty_file():
    qnetwork = keras.Sequential()
    qnetwork.add(keras.layers.Dense(24, input_shape=(20 * 20,), activation='relu'))
    qnetwork.add(keras.layers.Dense(24, activation='relu'))
    qnetwork.add(keras.layers.Dense(4, activation='linear'))
    qnetwork.compile(optimizer='adam', loss='mse')
    qnetwork.save('deepqnetwork.h5')
    with open('deepqnetworkcounter.json', 'w') as f:
        json.dump({'counter': 0}, f)


if __name__ == '__main__':
    generate_empty_file()
    print("File generated")
