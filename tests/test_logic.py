from random import seed as random_seed

import pytest
from conftest import Factory

from sudoku.logic import SudokuLogic


@pytest.fixture
def logic():
    return SudokuLogic()


@pytest.fixture
def sample_logic():
    logic = SudokuLogic()
    logic.board = [
        [0, 5, 4, 7, 8, 0, 0, 6, 3],
        [8, 0, 0, 0, 5, 0, 0, 7, 0],
        [7, 0, 0, 4, 0, 1, 2, 5, 0],
        [9, 3, 0, 0, 0, 6, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 4],
        [4, 1, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 7, 1, 6, 4, 0, 8, 2],
        [2, 4, 5, 8, 7, 0, 0, 1, 6],
        [6, 0, 0, 2, 0, 0, 7, 0, 9],
    ]
    logic.solution = [
        [1, 5, 4, 7, 8, 2, 9, 6, 3],
        [8, 2, 9, 6, 5, 3, 4, 7, 1],
        [7, 6, 3, 4, 9, 1, 2, 5, 8],
        [9, 3, 8, 5, 4, 6, 1, 2, 7],
        [5, 7, 2, 9, 1, 8, 6, 3, 4],
        [4, 1, 6, 3, 2, 7, 8, 9, 5],
        [3, 9, 7, 1, 6, 4, 5, 8, 2],
        [2, 4, 5, 8, 7, 9, 3, 1, 6],
        [6, 8, 1, 2, 3, 5, 7, 4, 9],
    ]
    return logic


class TestSudokuLogicGetHint:
    """Test SudokuLogic.get_hint."""

    def test_get_hint(self, sample_logic):
        random_seed(1234567809)

        assert sample_logic.get_hint() == (1, 1, 2)


class TestSudokuLogicGenerate:
    """Test SudokuLogic.generate."""

    def test_generate_with_seed(self, logic, sample_logic):
        seed = 1234567809
        num_clues = 40
        keep_pos = logic.generate(seed, num_clues)
        assert len(keep_pos) == num_clues
        assert logic.board == sample_logic.board


class TestSudokuLogicPossible:
    """Test SudokuLogic.possible."""

    def test_possible(self, sample_logic):
        assert sample_logic.possible(1, 0, 0) is True

    def test_col_exclude(self, sample_logic):
        assert sample_logic.possible(9, 0, 0) is False

    def test_row_exclude(self, sample_logic):
        assert sample_logic.possible(3, 0, 0) is False

    def test_box_exclude(self, sample_logic):
        assert sample_logic.possible(3, 4, 0) is False


class TestSudokuLogicIterateBoard:
    """Test SudokuLogic.iterate_board."""

    def test_next_value(self):
        assert next(SudokuLogic.iterate_board()) == (0, 0)


class TestSudokuLogicFindEmpty:
    """Test SudokuLogic.find_empty."""

    def test_found(self, logic):
        assert logic.find_empty() == (0, 0)

    def test_not_found(self, logic):
        for i, j in logic.iterate_board():
            logic.board[i][j] = 1
        assert logic.find_empty() is None


class TestSudokuLogicResetBoard:
    """Test SudokuLogic.reset_board."""

    def test_reset(self, logic):
        logic.board = Factory.create_random_board()
        logic.reset_board()
        assert logic.board == Factory.create_empty_board()


class TestSudokuLogicFillBoard:
    """Test SudokuLogic.fill_board."""

    def test_fill(self, logic):
        solution_board = Factory.create_random_board()
        logic.board = Factory.create_random_board()
        logic.solution = solution_board
        logic.fill_board()
        assert logic.board == solution_board


class TestSudokuLogicSolveBoard:
    """Test SudokuLogic.solve_board."""

    def test_solve(self, sample_logic):
        sample_logic.solve_board()
        assert sample_logic.board == sample_logic.solution
