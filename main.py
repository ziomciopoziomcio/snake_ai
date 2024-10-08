import pygame
from components import snake_helper, board_helper, parameters
import tkinter as tk

# game variables
# Zmienne te będą sterować zachowaniem gry.
board_width = 20
board_height = 20
snake_speed = 8
amount_of_food = 1
snake_amount = 1
score_type = 1
'''
SCORE TYPE:
0 - no score
1 - score in pygame window
2 - score in tkinter window 
'''
game_mode = 0
'''
GAME MODE:
0 - single player
1 - PvP
2 - PvAI
3 - AIvAI
4 - AI
'''
available_colours = [(24, 139, 34), (0, 0, 255)]

# pygame variables

window_width = 800
window_height = 800


# game objects

class Snake:
    def __init__(self, position=None):
        self.length = 1
        self.positions = [position] if position else [
            snake_helper.random_position(board_height, board_width, border_distance=3)]
        self.direction = self.get_valid_initial_direction()
        self.score = 0
        self.colour = None
        self.available_colour()
        self.alive = True

    def available_colour(self):
        self.colour = available_colours[0]
        available_colours.remove(self.colour)

    def get_initial_length(self):
        if board_height < 10 and board_width < 10:
            return 3
        elif 10 <= board_height <= 30 and 10 <= board_width <= 30:
            return 5
        else:
            return 10

    def get_valid_initial_direction(self):
        initial_position = self.positions[0]
        length = self.get_initial_length()
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if initial_position[0] < length:
            directions.remove('LEFT')
        if initial_position[0] > board_width - length - 1:
            directions.remove('RIGHT')
        if initial_position[1] < length:
            directions.remove('UP')
        if initial_position[1] > board_height - length - 1:
            directions.remove('DOWN')
        return snake_helper.random_direction(directions)

    def move(self, direction):
        if not self.alive:
            return
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
        self.snakes = []
        existing_positions = []
        for _ in range(self.snake_amount):
            pos = snake_helper.random_position(board_height, board_width, existing_positions, border_distance=3)
            existing_positions.append(pos)
            direction = snake_helper.random_direction(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.snakes.append(Snake(position=pos))
            # self.snakes.append(Snake(position=pos, direction=direction))
        self.food_amount = amount_of_food
        self.food = [self.generate_food_position() for _ in range(self.food_amount)]
        self.game_over = False
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

    def generate_food_position(self):
        while True:
            position = snake_helper.random_position(board_height, board_width)
            if all(position not in snake.positions for snake in self.snakes):
                return position

    def draw(self, screen):
        cell_size = min(window_width / board_width, window_height / board_height)
        for snake in self.snakes:
            for pos in snake.positions:
                pygame.draw.rect(screen, snake.colour, (pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size))
        for food in self.food:
            pygame.draw.rect(screen, (255, 0, 0), (food[0] * cell_size, food[1] * cell_size, cell_size, cell_size))

    def draw_score(self, screen):
        if game_mode == 0:
            score_text = f'Score: {self.snakes[0].score}'
            score_surface = self.font.render(score_text, True, (0, 0, 0))
            score_rect = score_surface.get_rect(center=(window_width // 2, 20))
            screen.blit(score_surface, score_rect)

        elif game_mode == 1:
            score_text = f'Score: P1 - {self.snakes[0].score} P2 - {self.snakes[1].score}'
            score_surface = self.font.render(score_text, True, (0, 0, 0))
            score_rect = score_surface.get_rect(center=(window_width // 2, 20))
            screen.blit(score_surface, score_rect)

    def is_game_over_snake(self, snake):
        if not snake.alive:
            return False
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
        next_position = list(head_position)
        if snake.direction == 'UP':
            next_position[1] -= 1
        elif snake.direction == 'DOWN':
            next_position[1] += 1
        elif snake.direction == 'LEFT':
            next_position[0] -= 1
        elif snake.direction == 'RIGHT':
            next_position[0] += 1
        if next_position in snake.positions[1:]:
            return True

        if any(next_position == pos for s in self.snakes if s != snake for pos in s.positions):
            return True
        return False

    def is_game_over(self):
        i = 0
        for snake in self.snakes:
            if not snake.alive:
                i += 1
        if i == len(self.snakes):
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
    board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width, score_type, game_mode = parameters.parameters_menu(
        board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width, score_type,
        game_mode)


# game mode 0 - single player
def handle_single_player_events(game, event, direction_changed):
    current_direction = game.snakes[0].direction
    if (event.key == pygame.K_w or event.key == pygame.K_UP) and current_direction != 'DOWN':
        direction_changed = True
        game.snakes[0].direction = 'UP'
    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and current_direction != 'UP':
        direction_changed = True
        game.snakes[0].direction = 'DOWN'
    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and current_direction != 'RIGHT':
        direction_changed = True
        game.snakes[0].direction = 'LEFT'
    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and current_direction != 'LEFT':
        direction_changed = True
        game.snakes[0].direction = 'RIGHT'
    return direction_changed


# game mode 1 - multiplayer
def handle_pvp_events(game, event, direction_changed, direction_changed2):
    current_direction = game.snakes[0].direction
    current_direction2 = game.snakes[1].direction
    if not direction_changed:
        if event.key == pygame.K_w and current_direction != 'DOWN':
            direction_changed = True
            game.snakes[0].direction = 'UP'
        elif event.key == pygame.K_s and current_direction != 'UP':
            direction_changed = True
            game.snakes[0].direction = 'DOWN'
        elif event.key == pygame.K_a and current_direction != 'RIGHT':
            direction_changed = True
            game.snakes[0].direction = 'LEFT'
        elif event.key == pygame.K_d and current_direction != 'LEFT':
            direction_changed = True
            game.snakes[0].direction = 'RIGHT'
    if not direction_changed2:
        if event.key == pygame.K_UP and current_direction2 != 'DOWN':
            direction_changed2 = True
            game.snakes[1].direction = 'UP'
        elif event.key == pygame.K_DOWN and current_direction2 != 'UP':
            direction_changed2 = True
            game.snakes[1].direction = 'DOWN'
        elif event.key == pygame.K_LEFT and current_direction2 != 'RIGHT':
            direction_changed2 = True
            game.snakes[1].direction = 'LEFT'
        elif event.key == pygame.K_RIGHT and current_direction2 != 'LEFT':
            direction_changed2 = True
            game.snakes[1].direction = 'RIGHT'
    return direction_changed, direction_changed2


def update_snakes(game):
    for snake in game.snakes:
        if game.is_game_over_snake(snake):
            snake.alive = False
        game.point_check(snake)
        snake.move(snake.direction)


def run():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    game = Game()
    running = True

    # potential tkinter window
    if score_type == 2:
        root = tk.Tk()
        root.title('Score')
        root.geometry('300x50')
        root.resizable(False, False)
        score_label = tk.Label(root, text=f'Score: {game.snakes[0].score}')
        score_label.pack()

    while running:
        direction_changed = False
        direction_changed2 = False if game_mode == 1 else None
        screen.fill((0, 0, 0))
        board_helper.draw_border(screen, (255, 255, 255), board_width, board_height, window_width, window_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_mode == 0:  # single player
                    direction_changed = handle_single_player_events(game, event, direction_changed)
                elif game_mode == 1:  # multiplayer
                    direction_changed, direction_changed2 = handle_pvp_events(game, event, direction_changed, direction_changed2)

        update_snakes(game)

        if game.is_game_over():
            game.game_over = True
            running = False

        game.draw(screen)
        if score_type == 1:
            game.draw_score(screen)
        elif score_type == 2:
            if game_mode == 0:
                score_label.config(text=f'Score: {game.snakes[0].score}')
                score_label.update()
            elif game_mode == 1:
                score_label.config(text=f'Score:\nP1 - {game.snakes[0].score}\nP2 - {game.snakes[1].score}')
                score_label.update()

        pygame.display.update()
        clock.tick(snake_speed)
    if game_mode == 1:
        return game.snakes[0].score, game.snakes[1].score
    elif game_mode == 0:
        return game.snakes[0].score
    else:
        return 0


run()