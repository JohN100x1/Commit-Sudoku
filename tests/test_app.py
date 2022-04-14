from sudoku.app import Actions, SudokuApp
from sudoku.view import SudokuBoard


class TestSudokuAppButtonAction:
    """Test SudokuApp.button_action."""

    def test_generate_board(self, mocker):
        mock = mocker.spy(SudokuBoard, "generate")
        app = SudokuApp()
        app.button_action(Actions.NEW_GAME)
        assert mock.call_count == 2

    def test_solve_board(self, mocker):
        mock = mocker.spy(SudokuBoard, "solve")
        app = SudokuApp()
        app.button_action(Actions.SOLVE)
        assert mock.call_count == 1

    def test_hint_board(self, mocker):
        mock = mocker.spy(SudokuBoard, "hint")
        app = SudokuApp()
        app.button_action(Actions.HINT)
        assert mock.call_count == 1
