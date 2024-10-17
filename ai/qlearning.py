import numpy as np
import random
import json
import os


class SnakeEnv:
    def __init__(self):
        self.qvalues = {}
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
        value = max(self.qvalues[state])
        index = random.choice([i for i, v in enumerate(self.qvalues[state]) if v == value])
        return index

    def save(self):
        with open('ai/qvalues.json', 'w') as f:
            json.dump(self.qvalues, f)

    def load(self):
        file_path = os.path.abspath('ai/qvalues.json')
        print(f"Looking for 'qvalues.json' in: {file_path}")
        with open(file_path, 'r') as f:
            self.qvalues = json.load(f)


def generate_empty_file():
    with open('qvalues.json', 'w') as f:
        empty = {}
        json.dump(empty, f)


if __name__ == '__main__':
    generate_empty_file()