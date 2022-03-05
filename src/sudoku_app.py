import logging
import random
from tkinter import Button, LabelFrame, Tk

from sudoku_board import SudokuBoard

DIGITS = {str(i) for i in range(1, 11)}

logger = logging.getLogger(__name__)


class SudokuApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")

        logger.info("Creating Solution box")
        self.solution = [["" for j in range(9)] for i in range(9)]

        logger.info("Creating Frames")
        self.frames = [
            [LabelFrame(text="Sudoku Board")],
            [LabelFrame(text="Actions")],
        ]

        self.board = SudokuBoard()
        self.actions = LabelFrame(text="Actions")

        # Creating Actions Buttons
        self.buttons = ["New Game", "Solve", "Hint"]
        self.button_frame = []
        for j, b in enumerate(self.buttons):
            self.button_frame.append(
                Button(
                    self.actions,
                    text=b,
                    padx=10,
                    pady=5,
                    command=lambda x=b: self.button_action(x),
                )
            )
            self.button_frame[j].grid(row=1, column=j, padx=38, pady=10)

        self.actions.grid(row=1, column=1, padx=50, pady=10)

        # Generate Board and GUI
        self.generate_board()

    def generate_board(self, seed=None, num_clues=17):
        if seed is not None:
            random.seed(seed)
        # Get random positions to keep
        entry_sample = random.sample(range(81), num_clues)
        keep_pos = {(x // 9, x % 9) for x in entry_sample}
        # Refresh the board
        for i in range(9):
            for j in range(9):
                self.board.sv[i][j].set("")
                self.board.board[i][j]["state"] = "normal"
        # Solve the board
        is_solved = self.solve_board(rand=True)
        # Partially erasing solved board
        for i in range(9):
            for j in range(9):
                self.solution[i][j] = self.board.sv[i][j].get()
                if (i, j) not in keep_pos:
                    self.board.sv[i][j].set("")
                else:
                    self.board.board[i][j]["state"] = "disabled"
                self.board.board[i][j]["bg"] = "white"
        if is_solved:
            print("Board Generated.")

    def find_empty(self):
        # Find empty position
        for i in range(9):
            for j in range(9):
                if self.board.sv[i][j].get() == "":
                    return i, j
        return None

    def solve_board(self, rand=False):
        # Find Empty positions
        empty_pos = self.find_empty()
        if empty_pos is None:
            return True
        else:
            i, j = empty_pos

        # Try random digits or not
        digits = [str(i) for i in range(1, 10)]
        if rand:
            random.shuffle(digits)

        # Solve via back-tracking
        for d in digits:
            if self.board.possible(d, i, j):
                self.board.sv[i][j].set(d)
                if self.solve_board(rand=rand):
                    return True
                self.board.sv[i][j].set("")
        return False

    def button_action(self, action):
        if action == "New Game":
            self.generate_board()
        elif action == "Solve":
            for i in range(9):
                for j in range(9):
                    if self.board.sv[i][j].get() == "":
                        self.board.sv[i][j].set(self.solution[i][j])
        elif action == "Hint":
            entry_sample = random.sample(range(81), 81)
            pos = {(x // 9, x % 9) for x in entry_sample}
            for i, j in pos:
                if self.board.sv[i][j].get() == "":
                    self.board.sv[i][j].set(self.solution[i][j])
                    break
        else:
            pass


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    app = SudokuApp()
    app.mainloop()
