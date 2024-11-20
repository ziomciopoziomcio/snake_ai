import tkinter as tk
from tkinter import messagebox


def parameters_menu(board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width,
                    score_type, game_mode):
    def submit(event=None):
        nonlocal board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width, score_type, game_mode
        try:
            board_width = int(board_width_entry.get())
            board_height = int(board_height_entry.get())
            snake_speed = int(snake_speed_entry.get())
            amount_of_food = int(amount_of_food_entry.get())
            # snake_amount = int(snake_amount_entry.get())
            window_height = int(window_height_entry.get())
            window_width = int(window_width_entry.get())
        except ValueError:
            messagebox.showerror("Error", "All values must be integers\nUsing default values")
            board_width = 20
            board_height = 20
            snake_speed = 5
            amount_of_food = 1
            snake_amount = 1
            window_height = 600
            window_width = 800
            score_type = 0
            game_mode = 0
            return

        if board_width < 6:
            messagebox.showerror("Error", "Board width must be at least 6\nUsing default value")
            board_width = 20
        if board_height < 6:
            messagebox.showerror("Error", "Board height must be at least 6\nUsing default value")
            board_height = 20
        if snake_speed < 0:
            messagebox.showerror("Error", "Snake speed must be a positive integer\nUsing default value")
            snake_speed = 5
        if amount_of_food < 0:
            messagebox.showerror("Error", "Amount of food must be a positive integer\nUsing default value")
            amount_of_food = 1
        # if snake_amount < 0:
        #     messagebox.showerror("Error", "Snake amount must be a positive integer\nUsing default value")
        #     snake_amount = 1
        if window_height < 0:
            messagebox.showerror("Error", "Window height must be a positive integer\nUsing default value")
            window_height = 600
        if window_width < 0:
            messagebox.showerror("Error", "Window width must be a positive integer\nUsing default value")
            window_width = 800

        score_type = {"Disabled": 0, "In game": 1, "In window": 2}.get(score_type_var.get(), 0)
        game_mode = {"Single player": 0, "PvP": 1, "PvAI": 2, "AIvAI": 3, "AI": 4, "QLearning": 5,
                     "deepQNetwork": 6}.get(game_mode_var.get(), 0)
        if game_mode == 0:
            snake_amount = 1
        elif game_mode == 1:
            snake_amount = 2
        if game_mode == 2 or game_mode == 3 or game_mode == 4:
            messagebox.showerror("Error", "AI is not implemented yet\nUsing default value")
            game_mode = 0

        root.destroy()

    root = tk.Tk()
    root.title('Parameters')
    root.geometry('300x450')
    root.resizable(False, False)

    tk.Label(root, text="Board Width:").pack()
    board_width_entry = tk.Entry(root)
    board_width_entry.insert(0, str(board_width))
    board_width_entry.pack()

    tk.Label(root, text="Board Height:").pack()
    board_height_entry = tk.Entry(root)
    board_height_entry.insert(0, str(board_height))
    board_height_entry.pack()

    tk.Label(root, text="Snake Speed:").pack()
    snake_speed_entry = tk.Entry(root)
    snake_speed_entry.insert(0, str(snake_speed))
    snake_speed_entry.pack()

    tk.Label(root, text="Amount of Food:").pack()
    amount_of_food_entry = tk.Entry(root)
    amount_of_food_entry.insert(0, str(amount_of_food))
    amount_of_food_entry.pack()

    # tk.Label(root, text="Snake Amount:").pack()
    # snake_amount_entry = tk.Entry(root)
    # snake_amount_entry.insert(0, str(snake_amount))
    # snake_amount_entry.pack()

    tk.Label(root, text="Window Height:").pack()
    window_height_entry = tk.Entry(root)
    window_height_entry.insert(0, str(window_height))
    window_height_entry.pack()

    tk.Label(root, text="Window Width:").pack()
    window_width_entry = tk.Entry(root)
    window_width_entry.insert(0, str(window_width))
    window_width_entry.pack()

    tk.Label(root, text="Score Type:").pack()
    score_type_var = tk.StringVar(value={0: "Disabled", 1: "In game", 2: "In window"}.get(score_type, "Disabled"))
    score_type_menu = tk.OptionMenu(root, score_type_var, "Disabled", "In game", "In window")
    score_type_menu.pack()

    tk.Label(root, text="Game Mode:").pack()
    game_mode_var = tk.StringVar(
        value={0: "Single player", 1: "PvP", 2: "PvAI", 3: "AIvAI", 4: "AI", 5: "QLearning", 6: "deepQNetwork"}.get(
            game_mode,
            "Single player"))
    game_mode_menu = tk.OptionMenu(root, game_mode_var, "Single player", "PvP", "PvAI", "AIvAI", "AI", "QLearning",
                                   "deepQNetwork")
    game_mode_menu.pack()

    tk.Button(root, text="Start game", command=submit).pack()
    root.bind('<Return>', submit)

    root.mainloop()

    return board_width, board_height, snake_speed, amount_of_food, snake_amount, window_height, window_width, score_type, game_mode
