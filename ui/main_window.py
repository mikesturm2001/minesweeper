# ui/main_window.py
import tkinter as tk
from tkinter import messagebox
from ui.game_board import GameBoard


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.geometry("600x500")

        self.game_board_frame = GameBoard(self)
        self.game_board_frame.pack()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
