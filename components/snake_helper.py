import random

def random_position(height, width):
    return [random.randint(0, height - 1), random.randint(0, width - 1)]

def random_direction():
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])