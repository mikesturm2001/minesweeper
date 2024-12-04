# ui/game_board.py
import tkinter as tk
from tkinter import messagebox
from core.game import Game

class GameBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.game = Game(10, 10, 10)  # 10x10 grid, 10 mines
        self.buttons = [[None for _ in range(self.game.board.cols)] for _ in range(self.game.board.rows)]
        self.create_widgets()

    def create_widgets(self):
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                btn = tk.Button(self, text="?", width=1, height=1, font=("Arial", 16), command=lambda r=row, c=col: self.reveal_cell(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

                # Bind right-click to flag the cell
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.flag_cell(r, c))

    def reveal_cell(self, row, col):
        if self.game.is_game_over:
            return  # Do nothing if the game is over

        game_over, message = self.game.reveal_cell(row, col)
        if game_over:
            messagebox.showerror("Game Over", message)
        else:
            # After revealing a cell, refresh all buttons to reflect the updated state
            self.refresh_buttons()

    def flag_cell(self, row, col):
        if self.game.is_game_over:
            return  # Do nothing if the game is over

        self.game.flag_cell(row, col)  # Toggle the flag state of the cell
        self.update_button(row, col)  # Update the button's appearance

    def update_button(self, row, col):
        # Get the cell object
        cell = self.game.board.grid[row][col]
        btn = self.buttons[row][col]

        # Use the __str__ method of the Cell to update the button text
        # If there are adjacent mines, set the number and apply the correct color
        color_map = {
            "1": "blue",
            "2": "green",
            "3": "red",
            "4": "dark blue",
            "5": "purple",
            "6": "teal",
            "7": "black",
            "8": "gray",
            "F": "orange"
        }

        btn.config(text=str(cell), bg="white" if cell.is_revealed else "gray", fg=color_map.get(str(cell), "black"))

    def refresh_buttons(self):
        # Loop through all cells and refresh their buttons
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                self.update_button(row, col)
