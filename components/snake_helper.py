import random


def random_position(height, width, existing_positions=None, min_distance=3):
    if existing_positions is None:
        existing_positions = []

    while True:
        position = [random.randint(1, height - 2), random.randint(1, width - 2)]
        if all([abs(position[0] - existing_position[0]) >= min_distance or abs(
                position[1] - existing_position[1]) >= min_distance for existing_position in existing_positions]):
            return position


def random_direction(directions):
    return random.choice(directions)
