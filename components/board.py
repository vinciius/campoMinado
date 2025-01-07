import tkinter as tk
from tkinter import messagebox
from random import sample
from components.cell import Cell

class Board(tk.Frame):
    def __init__(self, rows, cols, mines, master=None):
        super().__init__(master)
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.cells = [[Cell(self.buttons[row][col]) for col in range(cols)] for row in range(rows)]
        self.mine_positions = set()
        self.first_click = True
        self.init_board()

    def init_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(
                    self,
                    text="",
                    width=2,
                    height=1,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
                # Update the button reference in the cell
                self.cells[row][col].button = button

    def calculate_adjacent_mines(self): # Calcula a quantidade de minas adjacentes
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.cells[row][col].is_mine:
                    mine_count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            new_row, new_col = row + dr, col + dc
                            if (0 <= new_row < self.rows and 
                                0 <= new_col < self.cols and 
                                (new_row, new_col) in self.mine_positions):
                                mine_count += 1
                    self.cells[row][col].mine_count = mine_count

    def on_cell_click(self, row, col):
        if self.first_click:
            self.generate_mines(exclude_position=(row, col))
            self.calculate_adjacent_mines()
            self.first_click = False

        cell = self.cells[row][col]
        if not cell.is_revealed:
            if (row, col) in self.mine_positions:
                self.game_over()
            else:
                self.reveal_cell(row, col)

    def reveal_cell(self, row, col):
        cell = self.cells[row][col]
        if cell.is_revealed or (row, col) in self.mine_positions:
            return

        cell.reveal()
        
        if cell.mine_count == 0:
            # Recursively reveal adjacent cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < self.rows and 
                        0 <= new_col < self.cols):
                        self.reveal_cell(new_row, new_col)

    def generate_mines(self, exclude_position):
        total_cells = self.rows * self.cols
        exclude_index = exclude_position[0] * self.cols + exclude_position[1]
        all_positions = list(range(total_cells))
        all_positions.remove(exclude_index)
        
        mine_indices = set(sample(all_positions, self.mines))
        self.mine_positions = {(index // self.cols, index % self.cols) for index in mine_indices}
        
        # Set mine status in cells
        for row, col in self.mine_positions:
            self.cells[row][col].is_mine = True

    def game_over(self):
        for row, col in self.mine_positions:
            self.cells[row][col].show_mine()
        messagebox.showinfo("Game Over", "Você perdeu!")
        self.reset()

    def reset(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells = [[Cell(None) for _ in range(self.cols)] for _ in range(self.rows)]
        self.mine_positions = set()
        self.first_click = True
        self.init_board()