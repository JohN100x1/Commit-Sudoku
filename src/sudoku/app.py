import logging
from enum import Enum
from tkinter import Button, LabelFrame, Tk

from sudoku.view import SudokuBoard

logger = logging.getLogger(__name__)


class Actions(str, Enum):
    NEW_GAME = "New Game"
    SOLVE = "Solve"
    HINT = "Hint"


class SudokuApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")

        logger.info("Creating Frames")

        self.board = SudokuBoard()
        self.actions = LabelFrame(text="Actions")

        # Creating Actions Buttons
        self.buttons = []
        for i, action in enumerate(Actions):
            self.buttons.append(
                Button(
                    self.actions,
                    text=action.value,
                    padx=10,
                    pady=5,
                    command=lambda x=action: self.button_action(x),
                )
            )
            self.buttons[i].grid(row=1, column=i, padx=38, pady=10)

        self.actions.grid(row=1, column=1, padx=50, pady=10)

        # Generate Board and GUI
        self.board.generate()

    def button_action(self, action: Actions):
        if action == Actions.NEW_GAME:
            self.board.generate(None, 17)

        elif action == Actions.SOLVE:
            self.board.solve()

        elif action == Actions.HINT:
            self.board.hint()

        else:
            pass


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    app = SudokuApp()
    app.mainloop()
