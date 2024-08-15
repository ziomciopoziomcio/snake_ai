import pygame
from components import snake_helper, board_helper, parameters

# game variables
# Zmienne te będą sterować zachowaniem gry.
board_width = 20
board_height = 20
snake_speed = 8
amount_of_food = 1
snake_amount = 1

# pygame variables

window_width = 800
window_height = 800


# game objects

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [snake_helper.random_position(board_height, board_width)]
        self.direction = snake_helper.random_direction()
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

    def get_head_position(self):
        return self.positions[0]

    # Patrzac przyszlosciowo, np kary dla graczy
    def update_length(self, new_length):
        if new_length > self.length:
            for _ in range(new_length - self.length):
                self.positions.append(self.positions[-1])
        elif new_length < self.length:
            self.positions = self.positions[:new_length]
        self.length = new_length


class Game:
    def __init__(self):
        self.snake_amount = snake_amount
        self.snakes = [Snake() for _ in range(self.snake_amount)]
        self.food_amount = amount_of_food
        self.food = [self.generate_food_position() for _ in range(self.food_amount)]
        self.game_over = False

    def generate_food_position(self):
        while True:
            position = snake_helper.random_position(board_height, board_width)
            if all(position not in snake.positions for snake in self.snakes):
                return position

    def draw(self, screen):
        for snake in self.snakes:
            for pos in snake.positions:
                pygame.draw.rect(screen, snake.color, (pos[0] * 40, pos[1] * 40, 40, 40))
        for food in self.food:
            pygame.draw.rect(screen, (255, 0, 0), (food[0] * 40, food[1] * 40, 40, 40))

    def is_game_over(self, snake):
        head_position = snake.get_head_position()
        if snake.direction == 'UP':
            if head_position[1] + 1 <= 2:
                return True
        elif snake.direction == 'DOWN':
            if head_position[1] - 1 >= board_height - 3:
                return True
        elif snake.direction == 'LEFT':
            if head_position[0] + 1 <= 2:
                return True
        elif snake.direction == 'RIGHT':
            if head_position[0] - 1 >= board_width - 3:
                return True
        if head_position in snake.positions[1:]:
            return True
        return False

    def point_check(self, snake):
        head_position = snake.get_head_position()
        for food in self.food:
            if head_position == food:
                snake.update_length(snake.length + 1)
                snake.score += 1
                self.food.remove(food)
                self.food.append(self.generate_food_position())
                return True
        return False


# parameters menu
turned_on = True

if turned_on:
    board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width = parameters.parameters_menu(
        board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width)

# pygame setup

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
game = Game()
running = True

while running:
    screen.fill((0, 0, 0))
    board_helper.draw_border(screen, (255, 255, 255), board_width, board_height, window_width, window_height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            current_direction = game.snakes[0].direction
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and current_direction != 'DOWN':
                game.snakes[0].direction = 'UP'
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and current_direction != 'UP':
                game.snakes[0].direction = 'DOWN'
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and current_direction != 'RIGHT':
                game.snakes[0].direction = 'LEFT'
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and current_direction != 'LEFT':
                game.snakes[0].direction = 'RIGHT'

    for snake in game.snakes:
        if game.is_game_over(snake):
            running = False
            break
        if game.point_check(snake):
            print(snake.score)
        snake.move(snake.direction)

    game.draw(screen)

    pygame.display.update()
    clock.tick(snake_speed)
