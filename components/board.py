import tkinter as tk
import components.cell as cell
from random import sample

class Board(tk.Frame):
    def __init__(self, rows, cols, mines, master=None):
        super().__init__(master)
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cells = [[cell.Cell() for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.first_click = True  # Controla o estado do primeiro clique
        self.init_board()

    def init_board(self):
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                # Cria os botões das células
                cell = tk.Button(
                    self, text="", width=2, height=1,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def on_cell_click(self, row, col):
        if self.first_click:
            # Gera minas após o primeiro clique
            self.generate_mines(exclude_position=(row, col))
            self.first_click = False

        if (row, col) in self.mine_positions:
            self.game_over()
        else:
            self.reveal_cell(row, col)

    def generate_mines(self, exclude_position):
        """
        Gera as minas no tabuleiro, excluindo a célula clicada pelo jogador.
        """
        total_cells = self.rows * self.cols
        exclude_index = exclude_position[0] * self.cols + exclude_position[1]
        all_positions = list(range(total_cells))
        all_positions.remove(exclude_index)

        # Seleciona posições das minas sem incluir a posição excluída
        mine_indices = set(sample(all_positions, self.mines))
        self.mine_positions = {(index // self.cols, index % self.cols) for index in mine_indices}

    def reveal_cell(self, row, col):
        """
        Revela uma célula. Futuramente pode ser expandida para revelar vizinhos.
        """
        self.cells[row][col].configure(text="✓", state="disabled")

    def reset(self):
        """
        Reinicia o tabuleiro.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.cells = []
        self.mine_positions = set()
        self.first_click = True
        self.init_board()

    def game_over(self):
        """
        Exibe todas as minas e mostra uma mensagem de derrota.
        """
        for r, c in self.mine_positions:
            self.cells[r][c].configure(text="💣", state="disabled")
        tk.messagebox.showinfo("Game Over", "Você perdeu!")
        self.reset()
