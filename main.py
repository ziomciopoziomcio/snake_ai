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
snake_amount = 1




# game objects

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = snake_helper.random_position(board_height, board_width)
        self.direction = [0, 1]
        self.score = 0
        self.color = (222, 78, 55)



class Game:
    def __init__(self):
        self.snake_amount = snake_amount
        self.snakes = [Snake() for _ in range(self.snake_amount)]
        self.food_amount = amount_of_food
        self.food = [snake_helper.random_position(board_height, board_width) for _ in range(self.food_amount)]
        self.game_over = False

# pygame setup

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
game = Game()
running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # update display
    pygame.display.update()
    clock.tick(snake_speed)