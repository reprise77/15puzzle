import tkinter as tk
import random
from itertools import chain
import time

SIZE = 4
TILE_SIZE = 100

WIN_STATE = list(range(1, SIZE * SIZE)) + [0]  # [1, 2, ..., 15, 0]


def generate_solvable_board():
    board = WIN_STATE[:]
    while True:
        random.shuffle(board)
        temp_board = [board[i:i + SIZE] for i in range(0, SIZE * SIZE, SIZE)]
        if is_solvable(temp_board):
            break
    return temp_board


def is_solvable(board):
    flattened_board = list(chain(*board))
    inversions = 0
    for i in range(len(flattened_board)):
        for j in range(i + 1, len(flattened_board)):
            if flattened_board[i] and flattened_board[j] and flattened_board[i] > flattened_board[j]:
                inversions += 1
    empty_row = (flattened_board.index(0) // SIZE) + 1
    return (inversions + empty_row) % 2 == 0


class FifteenPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Пятнашки")

        self.start_time = time.time()
        self.game_over = False


        self.timer_label = tk.Label(self.root, text="Время: 0 секунд", font=("Helvetica", 16))
        self.timer_label.grid(row=0, column=0, columnspan=SIZE, pady=10)

        self.board = generate_solvable_board()
        self.tiles = []
        self.empty_tile = None
        self.create_board()

        restart_button = tk.Button(self.root, text="Перезапустить", command=self.reset_game, font=("Helvetica", 16))
        restart_button.grid(row=SIZE + 1, column=0, columnspan=SIZE, pady=10)

        for i in range(SIZE):
            self.root.grid_columnconfigure(i, weight=1, uniform="uniform")
            self.root.grid_rowconfigure(i + 1, weight=1, uniform="uniform")

        self.update_timer()

    def create_board(self):
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                value = self.board[i][j]
                button = tk.Button(self.root, text=str(value), font=("Helvetica", 24),
                                   command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
                row.append(button)
                if value == 0:
                    self.empty_tile = (i, j)
                    button.config(text="", bg="SystemButtonFace")
            self.tiles.append(row)

    def update_board(self):
        for i in range(SIZE):
            for j in range(SIZE):
                tile = self.tiles[i][j]
                value = self.board[i][j]
                if value == 0:
                    self.empty_tile = (i, j)
                    tile.config(text="", bg="SystemButtonFace")
                else:
                    tile.config(text=str(value), bg="SystemButtonFace")

    def move_tile(self, i, j):
        if self.game_over:
            return

        empty_i, empty_j = self.empty_tile

        if (abs(empty_i - i) == 1 and empty_j == j) or (abs(empty_j - j) == 1 and empty_i == i):
            self.board[empty_i][empty_j], self.board[i][j] = self.board[i][j], self.board[empty_i][empty_j]
            self.update_board()

        if self.is_solved():
            self.display_win_message()

    def is_solved(self):
        return list(chain(*self.board)) == WIN_STATE

    def display_win_message(self):
        self.game_over = True
        win_label = tk.Label(self.root, text="ура победа", font=("Helvetica", 24))
        win_label.grid(row=SIZE + 2, column=0, columnspan=SIZE, pady=10)

    def reset_game(self):
        self.game_over = False
        self.board = generate_solvable_board()
        self.update_board()
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Время: {elapsed_time} секунд")
            self.root.after(1000, self.update_timer)


if __name__ == "__main__":
    root = tk.Tk()
    app = FifteenPuzzleApp(root)
    root.mainloop()
