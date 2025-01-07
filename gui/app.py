import tkinter as tk
from tkinter import messagebox
from components.board import Board

class MinesweeperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campo Minado")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Inicializar o tabuleiro
        self.board = Board(rows=9, cols=9, mines=10, master=self)
        self.board.pack(pady=20)
        
        # Reiniciar jogo
        self.reset_button = tk.Button(self, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack()

    def reset_game(self):
        self.board.reset()
