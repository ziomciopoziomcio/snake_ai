import numpy as np
import random
import json


class SnakeEnv:
    def __init__(self):
        self.qvalues = {}
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
        with open('qvalues.json', 'w') as f:
            json.dump(self.qvalues, f)

    def load(self):
        with open('qvalues.json', 'r') as f:
            self.qvalues = json.load(f)
