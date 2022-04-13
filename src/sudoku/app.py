import logging
from tkinter import Button, LabelFrame, Tk

from board import SudokuBoard

logger = logging.getLogger(__name__)


class SudokuApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")

        logger.info("Creating Frames")
        self.frames = [
            [LabelFrame(text="Sudoku Board")],
            [LabelFrame(text="Actions")],
        ]

        self.board = SudokuBoard()
        self.actions = LabelFrame(text="Actions")

        # Creating Actions Buttons
        self.buttons = []
        for i, action in enumerate(["New Game", "Solve", "Hint"]):
            self.buttons.append(
                Button(
                    self.actions,
                    text=action,
                    padx=10,
                    pady=5,
                    command=lambda x=action: self.button_action(x),
                )
            )
            self.buttons[i].grid(row=1, column=i, padx=38, pady=10)

        self.actions.grid(row=1, column=1, padx=50, pady=10)

        # Generate Board and GUI
        self.board.generate()

    def button_action(self, action: str):
        if action == "New Game":
            self.board.generate()

        elif action == "Solve":
            self.board.solve()

        elif action == "Hint":
            self.board.hint()

        else:
            pass


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    app = SudokuApp()
    app.mainloop()
