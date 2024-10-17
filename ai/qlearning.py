import numpy as np
import random
import json
import os


class SnakeEnv:
    def __init__(self):
        self.qvalues = {}
        self.counter = 0
        self.load()
        self.learning_rate = 0.1
        self.discount = 0.9

    def update(self, state, action, next_state, reward):
        if state not in self.qvalues:
            self.qvalues[state] = np.zeros(4)
        if next_state not in self.qvalues:
            self.qvalues[next_state] = np.zeros(4)
        self.qvalues[state][action] = self.qvalues[state][action] + self.learning_rate * (
                reward + self.discount * max(self.qvalues[next_state]) - self.qvalues[state][action])

    def get_action(self, state):
        if state not in self.qvalues:
            self.qvalues[state] = np.zeros(4)
        p = random.random()
        if p < 0.1:
            return random.randint(0, 3)
        else:
            value = max(self.qvalues[state])
            index = random.choice([i for i, v in enumerate(self.qvalues[state]) if v == value])
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
        self.counter = data.get('counter', 0) + 1


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
