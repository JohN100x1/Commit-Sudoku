import pytest

from sudoku.logic import SudokuLogic


@pytest.fixture
def logic():
    return SudokuLogic()


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
        logic.board = [[1 for _ in range(9)] for _ in range(9)]
        logic.reset_board()
        assert logic.board == [[0 for _ in range(9)] for _ in range(9)]


class TestSudokuLogicFillBoard:
    """Test SudokuLogic.fill_board."""

    def test_fill(self, logic):
        solution_board = [[i for i in range(9)] for _ in range(9)]
        logic.board = [[1 for _ in range(9)] for _ in range(9)]
        logic.solution = solution_board
        logic.fill_board()
        assert logic.board == solution_board
