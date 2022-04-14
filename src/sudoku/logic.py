import logging
from copy import deepcopy
from random import sample
from random import seed as random_seed
from random import shuffle
from typing import Generator, Optional

logger = logging.getLogger(__name__)


class SudokuLogic:
    def __init__(self):
        empty_board = [[0 for _ in range(9)] for _ in range(9)]
        self.board: list[list[int]] = deepcopy(empty_board)
        self.solution: list[list[int]] = deepcopy(empty_board)

    @staticmethod
    def iterate_board() -> Generator[tuple[int, int], None, None]:
        """
        Generate all co-ordinates by iterating through the board.

        :return: Yield 2-tuple integer co-ordinates.
        """
        for i in range(9):
            for j in range(9):
                yield i, j

    def find_empty(self) -> Optional[tuple[int, int]]:
        """
        Find the first empty position on the Sudoku board.

        :return: 2-tuple integers co-ordinates of empty position or None.
        """
        for i, j in self.iterate_board():
            if self.board[i][j] == 0:
                return i, j
        return None

    def reset_board(self):
        """Reset the entire board."""
        for i, j in self.iterate_board():
            self.board[i][j] = 0

    def fill_board(self):
        """Fill the entire board with the solution board."""
        self.board = deepcopy(self.solution)

    def possible(self, digit: int, i: int, j: int) -> bool:
        """
        Determine whether digit can be placed in position (i, j) on the board.

        :param digit: int, the digit to be determined placeable.
        :param i: int, row-coordinate on the Sudoku board.
        :param j: int, column-coordinate on the Sudoku board.
        :return: bool, determines whether digit can be placed.
        """
        # Check Rows
        for x in range(9):
            if x != i and digit == self.board[x][j]:
                return False
        # Check Columns
        for y in range(9):
            if y != j and digit == self.board[i][y]:
                return False
        # Check Box
        for x in range(3 * (i // 3), 3 * (i // 3) + 3):
            for y in range(3 * (j // 3), 3 * (j // 3) + 3):
                if x != i and y != j and digit == self.board[x][y]:
                    return False
        return True

    def solve_board(self) -> bool:
        """
        Solves the Sudoku board using backtracking.

        :return: bool, determines whether the Sudoku board is solved.
        """
        # Find Empty positions
        empty_pos = self.find_empty()
        if empty_pos is None:
            return True
        i, j = empty_pos

        # Try random digits
        digits = [i for i in range(1, 10)]
        shuffle(digits)

        # Solve via backtracking
        for d in digits:
            if self.possible(d, i, j):
                self.board[i][j] = d
                if self.solve_board():
                    return True
                self.board[i][j] = 0
        return False

    def generate(
        self, seed: Optional[int] = None, num_clues: int = 17
    ) -> set[tuple[int, int]]:
        """
        Randomly generate a new board for given seed and number of clues.
        Return the positions of the clues.
        """
        # Set Seed if specified
        if seed is not None:
            random_seed(seed)

        # Get random positions to keep
        keep_pos = {(x // 9, x % 9) for x in sample(range(81), num_clues)}

        # Reset the board
        self.reset_board()

        # Solve the board
        solved = self.solve_board()

        # Partially erase the solved board
        for i, j in self.iterate_board():
            self.solution[i][j] = self.board[i][j]
            if (i, j) not in keep_pos:
                self.board[i][j] = 0
        if solved:
            logger.info("Board Generated.")
        return keep_pos

    def get_hint(self) -> tuple[int, int, int]:
        """Randomly get solution for the first empty position on the board."""
        random_pos = [(x // 9, x % 9) for x in sample(range(81), 81)]
        for i, j in random_pos:
            if self.board[i][j] == 0:
                return i, j, self.solution[i][j]
