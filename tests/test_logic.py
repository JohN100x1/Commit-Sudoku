import pytest

from sudoku.logic import SudokuLogic


@pytest.fixture
def logic():
    return SudokuLogic()


@pytest.fixture
def sample_logic():
    logic = SudokuLogic()
    logic.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 9, 0, 0, 0, 0],
    ]
    return logic


class TestSudokuLogicGenerate:
    """Test SudokuLogic.generate."""

    def test_generate_with_seed(self, logic, sample_logic):
        seed = 1234567890
        keep_pos = logic.generate(seed, 5)
        assert keep_pos == {(6, 2), (8, 4), (3, 1), (2, 2), (8, 2)}
        assert logic.board == sample_logic.board


class TestSudokuLogicPossible:
    """Test SudokuLogic.possible."""

    def test_possible(self, sample_logic):
        assert sample_logic.possible(2, 8, 1) is True

    def test_col_exclude(self, sample_logic):
        assert sample_logic.possible(3, 8, 1) is False

    def test_row_exclude(self, sample_logic):
        assert sample_logic.possible(9, 8, 1) is False

    def test_box_exclude(self, sample_logic):
        assert sample_logic.possible(8, 8, 1) is False


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
