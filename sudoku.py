import numpy as np
from tkinter import Tk
from tkinter import Entry, StringVar
from tkinter import LabelFrame, Button

DIGITS = [str(d) for d in range(1,10)]

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        
        # Solved Board
        self.solution = [["" for j in range(9)] for i in range(9)]
        
        # String Variables for all entry boxes
        self.sv = [[StringVar() for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.sv[i][j].trace("w", lambda name, index, mode, i=i, j=j: self.detect(i, j))
        self.gui()
        self.generate_board()
        
    def gui(self):
        # Creating Frames
        self.frames = []
        self.headers = ["Sudoku Board", "Actions"]
        for i, header in enumerate(self.headers):
            self.frames.append([])
            self.frames[i].append(
                LabelFrame(
                    text=header,
                    )
                )
        # Creating Sudoku Board
        sudoku_frame = self.frames[0]
        sudoku_frame.append([LabelFrame(sudoku_frame[0], relief="solid") for j in range(9)])
        sudoku_frame.append([])
        for i in range(9):
            sudoku_frame[2].append([])
            for j in range(9):
                row, col = i // 3, j // 3
                k = 3*row + col
                sudoku_frame[2][i].append(
                    Entry(sudoku_frame[1][k],
                          width=2,
                          font=("Helvetica", 28),
                          justify="center",
                          textvariable=self.sv[i][j]
                          )
                    )
                sudoku_frame[2][i][j].bind("<1>", lambda event, i=i, j=j: self.colour_box(event, i, j))
                sudoku_frame[2][i][j].grid(row=i, column=j)
            sudoku_frame[1][i].grid(row=i//3,column=i%3)
        
        # Creating Actions Buttons
        self.buttons = ["New Game", "Solve", "Hint"]
        button_frame = self.frames[1]
        for j, b in enumerate(self.buttons):
            button_frame.append(
                Button(button_frame[0],
                    text=b,
                    padx=10,
                    pady=5,
                    command=lambda b=b: self.button_action(b)
                    )
                )
            button_frame[j+1].grid(row=1,column=j, padx=38, pady=10)
        
        # Packing Frames
        for k, frame in enumerate(self.frames):
            frame[0].grid(row=k,column=1, padx=50, pady=10)
    
    def detect(self, i, j):
        c = self.sv[i][j].get()
        # Entries must be a digit
        if not c.isdigit():
            self.sv[i][j].set("")
        # Entries have only 1 character
        elif len(c) > 0:
            c = c[0]
            # Digit isn't zero
            if c == "0":
                self.sv[i][j].set("")
            else:
                self.sv[i][j].set(c)
        # Detect incorrect digit
        if not self.possible(c, i, j) and c != "":
            self.frames[0][2][i][j]["bg"] = "#FF7F7F"
        else:
            self.frames[0][2][i][j]["bg"] = "#ADD8E6"
    
    def colour_box(self, event, i, j):
        # Re-colour selected boxes
        box = 3*(i//3) + j//3
        for row in range(9):
            for col in range(9):
                if row == i and col == j:
                    self.frames[0][2][row][col]["bg"] = "#ADD8E6"
                elif row != i and col == j:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                elif row == i and col != j:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                elif box == 3*(row//3) + col//3:
                    self.frames[0][2][row][col]["bg"] = "#daedf4"
                else:
                    self.frames[0][2][row][col]["bg"] = "white"
                d = self.frames[0][2][row][col].get()
                if d != "":
                    if not self.possible(d, row, col):
                        self.frames[0][2][row][col]["bg"] = "#FF7F7F"
                    
    def generate_board(self, seed=None, num_clues=17):
        if seed is not None:
            np.random.seed(seed)
        # Get random positions to keep
        entry_sample = np.random.choice(range(81), num_clues)
        keep_pos = {(x//9,x%9) for x in entry_sample}
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
        for x in range(3*(i//3),3*(i//3)+3):
            for y in range(3*(j//3),3*(j//3)+3):
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
        if rand:
            digits = np.random.permutation(DIGITS)
        else:
            digits = DIGITS
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
            hint_given = False
            while not hint_given:
                i, j = np.random.choice(range(9),size=2,replace=True)
                if self.sv[i][j].get() == "":
                    self.sv[i][j].set(self.solution[i][j])
                    hint_given = True
        else:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()