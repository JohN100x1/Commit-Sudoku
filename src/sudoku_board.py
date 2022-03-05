from tkinter import Entry, LabelFrame, StringVar

DIGITS = {str(i) for i in range(1, 11)}


class SudokuBoard:
    def __init__(self):
        self.sv = [[StringVar() for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.sv[i][j].trace(
                    "w", lambda name, index, mode, x=i, y=j: self.detect(x, y)
                )
        # Creating Sudoku Board
        self.frame = LabelFrame(text="Sudoku Board")
        self.sub_boxes = [
            LabelFrame(self.frame, relief="solid") for j in range(9)
        ]
        self.board: list[list[Entry]] = []
        for i in range(9):
            self.board.append([])
            for j in range(9):
                row, col = i // 3, j // 3
                self.board[i].append(
                    Entry(
                        self.sub_boxes[3 * row + col],
                        width=2,
                        font=("Helvetica", 28),
                        justify="center",
                        textvariable=self.sv[i][j],
                    )
                )
                self.board[i][j].bind(
                    "<1>", lambda event, i=i, j=j: self.colour_box(event, i, j)
                )
                self.board[i][j].grid(row=i, column=j)
            self.sub_boxes[i].grid(row=i // 3, column=i % 3)

        # Packing Frames
        self.frame.grid(row=0, column=1, padx=50, pady=10)

    def detect(self, i, j):
        digit = self.sv[i][j].get()

        # Entries must be a digit
        if digit not in DIGITS:
            self.sv[i][j].set("")
        else:
            self.sv[i][j].set(digit)

        # Detect incorrect digit
        if not self.possible(digit, i, j) and digit != "":
            self.board[i][j]["bg"] = "#FF7F7F"
        else:
            self.board[i][j]["bg"] = "#ADD8E6"

    def colour_box(self, event, i, j):
        # Re-colour selected boxes
        box = 3 * (i // 3) + j // 3
        for row in range(9):
            for col in range(9):
                if row == i and col == j:
                    self.board[row][col]["bg"] = "#ADD8E6"
                elif row != i and col == j:
                    self.board[row][col]["bg"] = "#daedf4"
                elif row == i and col != j:
                    self.board[row][col]["bg"] = "#daedf4"
                elif box == 3 * (row // 3) + col // 3:
                    self.board[row][col]["bg"] = "#daedf4"
                else:
                    self.board[row][col]["bg"] = "white"
                d = self.board[row][col].get()
                if d != "":
                    if not self.possible(d, row, col):
                        self.board[row][col]["bg"] = "#FF7F7F"

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
