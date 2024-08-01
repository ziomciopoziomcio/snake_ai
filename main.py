import pygame

import components.snake_helper
from components import snake_helper

# game variables
'''
Zmienne te będą sterować zachowaniem gry.
'''
board_width = 20
board_height = 20
snake_speed = 5
amount_of_food = 1


# game objects

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = snake_helper.random_position(board_height, board_width)
        self.direction = [0, 1]
        self.score = 0
        self.color = (17, 24, 47)



