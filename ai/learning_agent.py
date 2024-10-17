from main import run

board_width = 20
board_height = 20
snake_speed = 25
amount_of_food = 1
snake_amount = 1
score_type = 1
game_mode = 5
window_width = 800
window_height = 800
turned_on = False

for i in range(1002):
    run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width, window_height, score_type,
        game_mode)