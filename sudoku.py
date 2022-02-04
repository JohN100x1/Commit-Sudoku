import random
from tkinter import Button, Entry, LabelFrame, StringVar, Tk

DIGITS = {str(i) for i in range(1, 11)}


class SudokuApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")

        # Solved Board
        self.solution = [["" for j in range(9)] for i in range(9)]

        # String Variables for all entry boxes
        self.sv = [[StringVar() for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.sv[i][j].trace(
                    "w", lambda name, index, mode, x=i, y=j: self.detect(x, y)
                )

        # Creating Frames
        self.frames = []
        self.headers = ["Sudoku Board", "Actions"]
        for i, header in enumerate(self.headers):
            self.frames.append([])
            self.frames[i].append(LabelFrame(text=header))

        # Creating Sudoku Board
        sudoku_frame = self.frames[0]
        sudoku_frame.append(
            [LabelFrame(sudoku_frame[0], relief="solid") for j in range(9)]
        )
        sudoku_frame.append([])
        for i in range(9):
            sudoku_frame[2].append([])
            for j in range(9):
                row, col = i // 3, j // 3
                k = 3 * row + col
                sudoku_frame[2][i].append(
                    Entry(
                        sudoku_frame[1][k],
                        width=2,
                        font=("Helvetica", 28),
                        justify="center",
                        textvariable=self.sv[i][j],
                    )
                )
                sudoku_frame[2][i][j].bind(
                    "<1>", lambda event, i=i, j=j: self.colour_box(event, i, j)
                )
                sudoku_frame[2][i][j].grid(row=i, column=j)
            sudoku_frame[1][i].grid(row=i // 3, column=i % 3)

        # Creating Actions Buttons
        self.buttons = ["New Game", "Solve", "Hint"]
        button_frame = self.frames[1]
        for j, b in enumerate(self.buttons):
            button_frame.append(
                Button(
                    button_frame[0],
                    text=b,
                    padx=10,
                    pady=5,
                    command=lambda x=b: self.button_action(x),
                )
            )
            button_frame[j + 1].grid(row=1, column=j, padx=38, pady=10)

        # Packing Frames
        for k, frame in enumerate(self.frames):
            frame[0].grid(row=k, column=1, padx=50, pady=10)

        # Generate Board and GUI
        self.generate_board()

    def detect(self, i, j):
        digit = self.sv[i][j].get()

        # Entries must be a digit
        if digit not in DIGITS:
            self.sv[i][j].set("")
        else:
            self.sv[i][j].set(digit)

        # Detect incorrect digit
        if not self.possible(digit, i, j) and digit != "":
            self.frames[0][2][i][j]["bg"] = "#FF7F7F"
        else:
            self.frames[0][2][i][j]["bg"] = "#ADD8E6"

    def colour_box(self, event, i, j):
        # Re-colour selected boxes
        box = 3 * (i // 3) + j // 3
        for row in range(9):
            for col in range(9):
                if row == i and col == j:
                    self.frames[0][2][row][col]["bg"] = "#ADD8E6"
                elif row != i and col == j:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                elif row == i and col != j:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                elif box == 3 * (row // 3) + col // 3:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                else:
                    self.frames[0][2][row][col]["bg"] = "white"
                d = self.frames[0][2][row][col].get()
                if d != "":
                    if not self.possible(d, row, col):
                        self.frames[0][2][row][col]["bg"] = "#FF7F7F"

    def generate_board(self, seed=None, num_clues=17):
        if seed is not None:
            random.seed(seed)
        # Get random positions to keep
        entry_sample = random.sample(range(81), num_clues)
        keep_pos = {(x // 9, x % 9) for x in entry_sample}
        # Refresh the board
        for i in range(9):
            for j in range(9):
                self.sv[i][j].set("")
                self.frames[0][2][i][j]["state"] = "normal"
        # Solve the board
        is_solved = self.solve_board(rand=True)
        # Partially erasing solved board
        for i in range(9):
            for j in range(9):
                self.solution[i][j] = self.sv[i][j].get()
                if (i, j) not in keep_pos:
                    self.sv[i][j].set("")
                else:
                    self.frames[0][2][i][j]["state"] = "disabled"
                self.frames[0][2][i][j]["bg"] = "white"
        if is_solved:
            print("Board Generated.")

    def find_empty(self):
        # Find empty position
        for i in range(9):
            for j in range(9):
                if self.sv[i][j].get() == "":
                    return i, j
        return None

    def possible(self, d, i, j):
        # Check Rows
        for x in range(9):
            if x != i and d == self.sv[x][j].get():
                return False
        # Check Columns
        for y in range(9):
            if y != j and d == self.sv[i][y].get():
                return False
        # Check Box
        for x in range(3 * (i // 3), 3 * (i // 3) + 3):
            for y in range(3 * (j // 3), 3 * (j // 3) + 3):
                if x != i and y != j and d == self.sv[x][y].get():
                    return False
        return True

    def solve_board(self, rand=False):
        # Find Empty positions
        empty_pos = self.find_empty()
        if empty_pos is None:
            return True
        else:
            i, j = empty_pos

        # Try random digits or not
        digits = [str(i) for i in range(1, 10)]
        if rand:
            random.shuffle(digits)

        # Solve via back-tracking
        for d in digits:
            if self.possible(d, i, j):
                self.sv[i][j].set(d)
                if self.solve_board(rand=rand):
                    return True
                self.sv[i][j].set("")
        return False

    def button_action(self, action):
        if action == "New Game":
            self.generate_board()
        elif action == "Solve":
            for i in range(9):
                for j in range(9):
                    if self.sv[i][j].get() == "":
                        self.sv[i][j].set(self.solution[i][j])
        elif action == "Hint":
            entry_sample = random.sample(range(81), 81)
            pos = {(x // 9, x % 9) for x in entry_sample}
            for _ in pos:
                i, j = random.choices(range(9), k=2)
                if self.sv[i][j].get() == "":
                    self.sv[i][j].set(self.solution[i][j])
                    break
        else:
            pass


if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
