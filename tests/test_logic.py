import pytest

from sudoku.logic import SudokuLogic


class TestSudokuLogicIterateBoard:
    """Test SudokuLogic.iterate_board."""

    def test_next_value(self):
        assert next(SudokuLogic.iterate_board()) == (0, 0)


class TestSudokuLogicFindEmpty:
    """Test SudokuLogic.find_empty."""

    @pytest.fixture
    def logic(self):
        return SudokuLogic()

    def test_found(self, logic):
        assert logic.find_empty() == (0, 0)

    def test_not_found(self, logic):
        for i, j in logic.iterate_board():
            logic.board[i][j] = 1
        assert logic.find_empty() is None
