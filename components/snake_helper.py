import random


def random_position(height, width, existing_positions=None, min_distance=3, border_distance=3):
    if existing_positions is None:
        existing_positions = []

    while True:
        position = [
            random.randint(border_distance, height - border_distance - 1),
            random.randint(border_distance, width - border_distance - 1)
        ]
        if all([abs(position[0] - existing_position[0]) >= min_distance or abs(
                position[1] - existing_position[1]) >= min_distance for existing_position in existing_positions]):
            return position


def random_direction(directions):
    return random.choice(directions)


def random_colour():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)