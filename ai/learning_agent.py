from main import run
import time

board_width = 20
board_height = 20
snake_speed = 100000
amount_of_food = 1
snake_amount = 1
score_type = 1
game_mode = 5
window_width = 800
window_height = 800
turned_on = False

for j in range(10):
    if j != 0:
        print("Waiting 100")
        time.sleep(100)
    for z in range(10):
        print("Waiting 10")
        time.sleep(10)
        for i in range(100):
            run(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_width, window_height, score_type,
                game_mode)
