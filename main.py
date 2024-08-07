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
        self.positions = [snake_helper.random_position(board_height, board_width)]
        self.direction = 'UP'
        self.score = 0
        self.color = (222, 78, 55)

    def move(self, direction):
        current_position = self.positions[0]
        if direction == 'UP':
            new_position = [current_position[0], current_position[1] - 1]
        elif direction == 'DOWN':
            new_position = [current_position[0], current_position[1] + 1]
        elif direction == 'LEFT':
            new_position = [current_position[0] - 1, current_position[1]]
        elif direction == 'RIGHT':
            new_position = [current_position[0] + 1, current_position[1]]
        self.positions = [new_position] + self.positions[:-1]


class Game:
    def __init__(self):
        self.snake_amount = snake_amount
        self.snakes = [Snake() for _ in range(self.snake_amount)]
        self.food_amount = amount_of_food
        self.food = [snake_helper.random_position(board_height, board_width) for _ in range(self.food_amount)]
        self.game_over = False

    def draw(self, screen):
        for snake in self.snakes:
            for pos in snake.positions:
                pygame.draw.rect(screen, snake.color, (pos[0] * 40, pos[1] * 40, 40, 40))
        for food in self.food:
            pygame.draw.rect(screen, (255, 0, 0), (food[0] * 40, food[1] * 40, 40, 40))


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                game.snakes[0].direction = 'UP'
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                game.snakes[0].direction = 'DOWN'
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                game.snakes[0].direction = 'LEFT'
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                game.snakes[0].direction = 'RIGHT'

    for snake in game.snakes:
        snake.move(snake.direction)

    game.draw(screen)

    pygame.display.update()
    clock.tick(snake_speed)

    # update display
    pygame.display.update()
    clock.tick(snake_speed)
