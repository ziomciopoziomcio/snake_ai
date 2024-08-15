import random

def random_position(height, width):
    return [random.randint(1, height - 2), random.randint(1, width - 2)]

def random_direction(directions):
    return random.choice(directions)