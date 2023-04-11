import logging
from tkinter import Entry, Event, LabelFrame, StringVar
from typing import Optional

from sudoku.logic import SudokuLogic

logger = logging.getLogger(__name__)


class SudokuBoard:
    DIGITS = {str(i) for i in range(1, 11)}

    COLOUR_RIGHT = "#ADD8E6"
    COLOUR_WRONG = "#FF7F7F"

    COLOUR_SELECTED = "#ADD8E6"
    COLOUR_ADJACENT = "#DAEDF4"
    COLOUR_DEFAULT = "#FFFFFF"

    def __init__(self):
        self.logic = SudokuLogic()

        # Create StringVar for each cell on Sudoku Board
        self.sv = [[StringVar() for _ in range(9)] for _ in range(9)]
        for i, j in self.logic.iterate_board():
            self.sv[i][j].trace(
                "w", lambda name, index, mode, x=i, y=j: self.detect(x, y)
            )

        # Create Entry boxes for each cell on Sudoku Board
        self.frame = LabelFrame(text="Sudoku Board")
        self.boxes = [LabelFrame(self.frame, relief="solid") for j in range(9)]
        self.entries: list[list[Entry]] = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i].append(
                    Entry(
                        self.boxes[3 * (i // 3) + (j // 3)],
                        width=2,
                        font=("Helvetica", 28),
                        justify="center",
                        textvariable=self.sv[i][j],
                    )
                )
                self.entries[i][j].bind(
                    "<1>", lambda event, x=i, y=j: self.highlight(event, x, y)
                )
                self.entries[i][j].grid(row=i, column=j)
            self.boxes[i].grid(row=i // 3, column=i % 3)

        # Pack Frames
        self.frame.grid(row=0, column=1, padx=50, pady=10)

    def solve_board(self):
        """Solve the Sudoku board."""
        self.logic.solve_board()
        for i, j in self.logic.iterate_board():
            self.sv[i][j].set(str(self.logic.solution[i][j]))

    def generate(self, seed: Optional[int] = None, num_clues: int = 17):
        keep_pos = self.logic.generate(seed, num_clues)
        # Refresh the board
        for i, j in self.logic.iterate_board():
            self.entries[i][j]["bg"] = "white"
            if (i, j) in keep_pos:
                self.sv[i][j].set(str(self.logic.solution[i][j]))
                self.entries[i][j]["state"] = "disabled"
            else:
                self.sv[i][j].set("")
                self.entries[i][j]["state"] = "normal"
        logger.info("Board Generated.")

    def hint(self):
        """Randomly fill solution for the first empty position on the board."""
        i, j, answer = self.logic.get_hint()
        self.logic.board[i][j] = answer
        self.sv[i][j].set(str(answer))

    def solve(self):
        """Solve the Sudoku board."""
        self.logic.fill_board()
        for i, j in self.logic.iterate_board():
            self.sv[i][j].set(str(self.logic.solution[i][j]))

    def detect(self, i: int, j: int):
        """When String variable in a cell changes, make sure it's a digit."""
        digit = self.sv[i][j].get()

        # Entries must be a digit
        if digit not in self.DIGITS:
            self.sv[i][j].set("")
            self.logic.board[i][j] = 0
            return
        self.sv[i][j].set(digit)
        self.logic.board[i][j] = int(digit)

        # Detect correct digits
        if self.logic.possible(int(digit), i, j):
            self.entries[i][j]["bg"] = self.COLOUR_RIGHT
        else:
            self.entries[i][j]["bg"] = self.COLOUR_WRONG

    def highlight(self, event: Event, i: int, j: int):
        """When an entry is clicked, re-colour cells."""
        logger.debug(f"{event} Event on cell ({i}, {j})")
        for row, col in self.logic.iterate_board():
            # The selected cell
            if row == i and col == j:
                self.entries[row][col]["bg"] = self.COLOUR_SELECTED

            # The cells within row, column, sub-box of selected cell
            elif row != i and col == j:
                self.entries[row][col]["bg"] = self.COLOUR_ADJACENT
            elif row == i and col != j:
                self.entries[row][col]["bg"] = self.COLOUR_ADJACENT
            elif 3 * (i // 3) + j // 3 == 3 * (row // 3) + col // 3:
                self.entries[row][col]["bg"] = self.COLOUR_ADJACENT

            # The remaining cells not within row, column, sub-box of cell
            else:
                self.entries[row][col]["bg"] = self.COLOUR_DEFAULT

            # Colour cells which are invalid
            digit = self.entries[row][col].get()
            if digit != "" and not self.logic.possible(int(digit), row, col):
                self.entries[row][col]["bg"] = self.COLOUR_WRONG
