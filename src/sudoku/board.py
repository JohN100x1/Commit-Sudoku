from random import sample
from random import seed as random_seed
from random import shuffle
from tkinter import Entry, Event, LabelFrame, StringVar
from typing import Optional

DIGITS = {str(i) for i in range(1, 11)}


class SudokuBoard:
    def __init__(self):
        self.solution = [["" for _ in range(9)] for _ in range(9)]
        self.sv = [[StringVar() for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.sv[i][j].trace(
                    "w", lambda name, index, mode, x=i, y=j: self.detect(x, y)
                )
        # Creating Sudoku Board
        self.frame = LabelFrame(text="Sudoku Board")
        self.sub_boxes = [
            LabelFrame(self.frame, relief="solid") for j in range(9)
        ]
        self.board: list[list[Entry]] = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.board[i].append(
                    Entry(
                        self.sub_boxes[3 * (i // 3) + (j // 3)],
                        width=2,
                        font=("Helvetica", 28),
                        justify="center",
                        textvariable=self.sv[i][j],
                    )
                )
                self.board[i][j].bind(
                    "<1>", lambda event, x=i, y=j: self.colour_box(event, x, y)
                )
                self.board[i][j].grid(row=i, column=j)
            self.sub_boxes[i].grid(row=i // 3, column=i % 3)

        # Packing Frames
        self.frame.grid(row=0, column=1, padx=50, pady=10)

    def find_empty(self) -> Optional[tuple[int, int]]:
        # Find empty position
        for i in range(9):
            for j in range(9):
                if self.sv[i][j].get() == "":
                    return i, j
        return None

    def solve_board(self, rand: bool = False) -> bool:
        # Find Empty positions
        empty_pos = self.find_empty()
        if empty_pos is None:
            return True
        else:
            i, j = empty_pos

        # Try random digits or not
        digits = [str(i) for i in range(1, 10)]
        if rand:
            shuffle(digits)

        # Solve via back-tracking
        for d in digits:
            if self.possible(d, i, j):
                self.sv[i][j].set(d)
                if self.solve_board(rand=rand):
                    return True
                self.sv[i][j].set("")
        return False

    def generate(self, seed: Optional[int] = None, num_clues: int = 17):
        if seed is not None:
            random_seed(seed)
        # Get random positions to keep
        entry_sample = sample(range(81), num_clues)
        keep_pos = {(x // 9, x % 9) for x in entry_sample}
        # Refresh the board
        for i in range(9):
            for j in range(9):
                self.sv[i][j].set("")
                self.board[i][j]["state"] = "normal"
        # Solve the board
        is_solved = self.solve_board(rand=True)
        # Partially erasing solved board
        for i in range(9):
            for j in range(9):
                self.solution[i][j] = self.sv[i][j].get()
                if (i, j) not in keep_pos:
                    self.sv[i][j].set("")
                else:
                    self.board[i][j]["state"] = "disabled"
                self.board[i][j]["bg"] = "white"
        if is_solved:
            print("Board Generated.")

    def hint(self):
        entry_sample = sample(range(81), 81)
        pos = {(x // 9, x % 9) for x in entry_sample}
        for i, j in pos:
            if self.sv[i][j].get() == "":
                self.sv[i][j].set(self.solution[i][j])
                break

    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.sv[i][j].get() == "":
                    self.sv[i][j].set(self.solution[i][j])

    def detect(self, i: int, j: int):
        digit = self.sv[i][j].get()

        # Entries must be a digit
        if digit not in DIGITS:
            self.sv[i][j].set("")
        else:
            self.sv[i][j].set(digit)

        # Detect incorrect digit
        if not self.possible(digit, i, j) and digit != "":
            self.board[i][j]["bg"] = "#FF7F7F"
        else:
            self.board[i][j]["bg"] = "#ADD8E6"

    def colour_box(self, event: Event, i: int, j: int):
        # Re-colour selected boxes
        box = 3 * (i // 3) + j // 3
        for row in range(9):
            for col in range(9):
                if row == i and col == j:
                    self.board[row][col]["bg"] = "#ADD8E6"
                elif row != i and col == j:
                    self.board[row][col]["bg"] = "#daedf4"
                elif row == i and col != j:
                    self.board[row][col]["bg"] = "#daedf4"
                elif box == 3 * (row // 3) + col // 3:
                    self.board[row][col]["bg"] = "#daedf4"
                else:
                    self.board[row][col]["bg"] = "white"
                digit = self.board[row][col].get()
                if digit != "":
                    if not self.possible(digit, row, col):
                        self.board[row][col]["bg"] = "#FF7F7F"

    def possible(self, digit: str, i: int, j: int) -> bool:
        # Check Rows
        for x in range(9):
            if x != i and digit == self.sv[x][j].get():
                return False
        # Check Columns
        for y in range(9):
            if y != j and digit == self.sv[i][y].get():
                return False
        # Check Box
        for x in range(3 * (i // 3), 3 * (i // 3) + 3):
            for y in range(3 * (j // 3), 3 * (j // 3) + 3):
                if x != i and y != j and digit == self.sv[x][y].get():
                    return False
        return True
