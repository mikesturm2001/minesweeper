# ui/game_board.py
import tkinter as tk
import tkmacosx
from tkinter import messagebox
from core.game import Game


class GameBoard(tk.Frame):
    COLOR_MAP = {
        "1": "blue",
        "2": "green",
        "3": "red",
        "4": "dark blue",
        "5": "purple",
        "6": "teal",
        "7": "black",
        "8": "gray",
        "F": "orange",
        "?": "black",  # Default hidden state
    }

    def __init__(self, master):
        super().__init__(master)
        self.rows = 10
        self.cols = 10
        self.num_mines = 10
        self.master = master
        self.game = Game(self.rows, self.cols, self.num_mines)  # 10x10 grid, 10 mines
        self.buttons = [[None for _ in range(self.game.board.cols)] for _ in range(self.game.board.rows)]
        self.create_widgets()
        self.update_timer_and_mines_left()

    def create_widgets(self):
        # Main frame for all top controls
        top_controls_frame = tk.Frame(self.master)
        top_controls_frame.pack(fill="x", pady=10)

        # Row for inputs (Rows, Columns, Mines, New Game)
        inputs_frame = tk.Frame(top_controls_frame)
        inputs_frame.pack()

        # Row input
        row_label = tk.Label(inputs_frame, text="Rows:")
        row_label.grid(row=0, column=0, padx=5)
        self.row_entry = tk.Entry(inputs_frame, width=5)
        self.row_entry.insert(0, str(self.rows))
        self.row_entry.grid(row=0, column=1, padx=5)

        # Column input
        col_label = tk.Label(inputs_frame, text="Columns:")
        col_label.grid(row=0, column=2, padx=5)
        self.col_entry = tk.Entry(inputs_frame, width=5)
        self.col_entry.insert(0, str(self.cols))
        self.col_entry.grid(row=0, column=3, padx=5)

        # Mines input
        mine_label = tk.Label(inputs_frame, text="Mines:")
        mine_label.grid(row=0, column=4, padx=5)
        self.mine_entry = tk.Entry(inputs_frame, width=5)
        self.mine_entry.insert(0, str(self.num_mines))
        self.mine_entry.grid(row=0, column=5, padx=5)

        # New Game button
        new_game_button = tk.Button(
            inputs_frame,
            text="New Game",
            command=self.start_new_game,
            bg="light gray",
        )
        new_game_button.grid(row=0, column=6, padx=10)

        # Row for Timer and Mines Left
        status_frame = tk.Frame(top_controls_frame)
        status_frame.pack(pady=5)

        # Timer
        self.timer_label = tk.Label(status_frame, text="Time: 0")
        self.timer_label.grid(row=0, column=0, padx=10)

        # Mines Left
        self.mines_left_label = tk.Label(status_frame, text=f"Mines Left: {self.game.mines_left}")
        self.mines_left_label.grid(row=0, column=1, padx=10)

    def create_game_grid(self):
        """Create the grid of buttons for the game board."""
        if hasattr(self, "grid_frame"):
            self.grid_frame.destroy()  # Remove the existing grid frame if it exists

        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(pady=10)

        # reset grid of buttons
        self.buttons = [[None for _ in range(self.game.board.cols)] for _ in range(self.game.board.rows)]

        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                btn = tkmacosx.Button(
                    self.grid_frame,
                    text="?",
                    font=("Helvetica", 14, "bold"),
                    height=30,
                    width=30,
                    bg="gray",
                    borderless=1,
                    command=lambda r=row, c=col: self.reveal_cell(r, c),
                )
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

                # Bind right-click to flag the cell
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.flag_cell(r, c))

    def start_new_game(self):
        """Start a new game with the specified settings."""
        try:
            rows = int(self.row_entry.get())
            cols = int(self.col_entry.get())
            num_mines = int(self.mine_entry.get())
            if rows < 1 or cols < 1 or num_mines < 1:
                raise ValueError("Values must be positive integers.")

            if num_mines >= rows * cols:
                raise ValueError("Mines must be fewer than total cells.")

            # Update game parameters
            self.rows = rows
            self.cols = cols
            self.num_mines = num_mines

            # Create new game
            self.game = Game(self.rows, self.cols, self.num_mines)

            # Resize board and refresh UI
            self.resize_board(rows, cols, num_mines)
            self.create_game_grid()

            # Reset Timer and Mines Left
            self.timer_label.config(text="Time: 0")  # Reset the timer display
            self.mines_left_label.config(text=f"Mines Left: {self.game.mines_left}")  # Reset mines left display

            # Restart the timer update loop
            self.update_timer_and_mines_left()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def update_timer_and_mines_left(self):
        if not self.game.is_game_over:
            # Update timer
            elapsed_time = self.game.get_elapsed_time()
            self.timer_label.config(text=f"Time: {elapsed_time}")

            # Update mines left
            self.mines_left_label.config(text=f"Mines Left: {self.game.mines_left}")

            # Call this method again after 1 second
            self.after(1000, self.update_timer_and_mines_left)

    def reveal_cell(self, row, col):
        if self.game.is_game_over:
            return  # Do nothing if the game is over

        game_over, message = self.game.reveal_cell(row, col)
        if game_over:
            # Game is over, reveal all cells
            self.reveal_entire_board()
            if message == "You hit a mine! Game over.":
                messagebox.showerror("Game Over", message)
            elif message == "You Win!":
                messagebox.showinfo("Congratulations!", "You won! 🎉")
        else:
            # After revealing a cell, refresh all buttons to reflect the updated state
            self.refresh_buttons()

    def reveal_entire_board(self):
        """Reveal all cells on the board."""
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                self.game.board.grid[row][col].is_revealed = True  # Mark all cells as revealed
                self.update_button(row, col)  # Update the button to display the cell's state

    def flag_cell(self, row, col):
        if self.game.is_game_over:
            return  # Do nothing if the game is over

        self.game.flag_cell(row, col)  # Toggle the flag state of the cell
        self.update_button(row, col)  # Update the button's appearance

    def update_button(self, row, col):
        # Get the cell object
        cell = self.game.board.grid[row][col]
        btn = self.buttons[row][col]

        btn.config(text=str(cell),
                   borderless=1,
                   bg="white" if cell.is_revealed else "gray",
                   fg=self.COLOR_MAP.get(str(cell), "black"))

    def refresh_buttons(self):
        # Loop through all cells and refresh their buttons
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                self.update_button(row, col)

    def resize_board(self, rows, cols, num_mines):
        """Dynamically resize the board."""
        # Update the game instance with the new configuration
        self.game = Game(rows, cols, num_mines)
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        # Recreate the game grid
        self.create_game_grid()
