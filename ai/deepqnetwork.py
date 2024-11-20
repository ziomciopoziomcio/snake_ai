import numpy as np
import random
import json
import os
import keras


class SnakeEnv:
    def __init__(self, qnetwork, counter, width, height, agent="off", exploration_rate=0.1):
        self.qnetwork = keras.Sequential()
        self.qnetwork.add(keras.layers.Dense(24, input_shape=(width*height,), activation='relu'))
        self.qnetwork.add(keras.layers.Dense(24, activation='relu'))
        self.qnetwork.add(keras.layers.Dense(4, activation='linear'))
        self.qnetwork.compile(optimizer='adam', loss='mse')
        self.counter = 0
        if agent == "off":
            self.load()
        else:
            self.qnetwork = qnetwork
            self.counter = counter
        self.learning_rate = 0.1
        self.discount = 0.9
        self.exploration_rate = exploration_rate

    def update(self, state, action, next_state, reward):
        result = self.qnetwork.predict(state)
        result_next = self.qnetwork.predict(next_state)
        result[action] = result[action] + self.learning_rate * (
                reward + self.discount * max(result_next) - result[action])
        self.qnetwork.fit(state, result, epochs=1, verbose=0)

    def get_action(self, state):
        p = random.random()
        if p < self.exploration_rate:
            return random.randint(0, 3)
        else:
            result = self.qnetwork.predict(state)
            value = max(result)
            index = random.choice([i for i, v in enumerate(result) if v == value])
            return index

    def save(self):
        file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
        qvalues_str_keys = {str(k): v.tolist() for k, v in self.qvalues.items()}
        data = {
            'qvalues': qvalues_str_keys,
            'counter': self.counter
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def load(self):
        file_path = os.path.join(os.path.dirname(__file__), 'qvalues.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        qvalues_str_keys = data.get('qvalues', {})
        self.qvalues = {eval(k): np.array(v) for k, v in qvalues_str_keys.items()}
        self.counter = data.get('counter', 0)


def generate_empty_file():
    qvalues_str_keys = {str(k): v for k, v in {}}
    data = {
        'qvalues': qvalues_str_keys,
        'counter': 0
    }
    with open('qvalues.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    generate_empty_file()
    print("File generated")
