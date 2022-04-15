import sys

import pytest

from sudoku.app import Actions, SudokuApp
from sudoku.view import SudokuBoard


@pytest.fixture
def app():
    return SudokuApp()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
class TestSudokuAppButtonAction:
    """Test SudokuApp.button_action."""

    def test_generate_board(self, mocker, app):
        mock = mocker.spy(SudokuBoard, "generate")
        app.button_action(Actions.NEW_GAME)
        assert mock.call_count == 1

    def test_solve_board(self, mocker, app):
        mock = mocker.spy(SudokuBoard, "solve")
        app.button_action(Actions.SOLVE)
        assert mock.call_count == 1

    def test_hint_board(self, mocker, app):
        mock = mocker.spy(SudokuBoard, "hint")
        app.button_action(Actions.HINT)
        assert mock.call_count == 1
