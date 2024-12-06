# core/game.py
from core.board import Board
import time

class Game:
    def __init__(self, rows, cols, num_mines):
        """
        Initialize a new game.
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_left = num_mines
        self.start_time = None
        self.board = self.initialize_board()  # Create the board
        self.is_game_over = False
        self.is_winner = False

    def reveal_cell(self, row, col):
        """
        Handles the logic for revealing a cell.
        Returns a tuple (game_over, message).
        """
        if self.is_game_over:
            return True, "The game is over! Start a new game."

        cell = self.board.grid[row][col]
        if cell.is_flagged:
            return False, "Cell is flagged. Unflag it first to reveal."

        if cell.is_mine:
            self.is_game_over = True
            return True, "You hit a mine! Game over."

        # Update the board and reveal adjacent cells if this cell is empty
        self.board.reveal_cell(row, col)

        # Check if the player has won
        self.check_win_condition()
        if self.is_winner:
            return True, "You Win!"

        return False, None  # Game continues

    def flag_cell(self, row, col):
        """
        Toggles a flag on a cell.
        Returns a message indicating the result.
        """
        if self.is_game_over:
            return "The game is over! Start a new game."

        cell = self.board.grid[row][col]
        cell.toggle_flag()

        if cell.is_flagged:
            self.mines_left = self.mines_left - 1
        else:
            self.mines_left = self.mines_left + 1
        return f"Flag {'set' if cell.is_flagged else 'removed'} on cell ({row}, {col})."

    def check_win_condition(self):
        """
        Check if all non-mine cells have been revealed.
        If the player has won, set the `is_winner` flag.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board.grid[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return  # Still cells to uncover, no win yet

        # If we reach here, the player has revealed all non-mine cells
        self.is_game_over = True
        self.is_winner = True
        return "Congratulations! You've won the game."

    def restart(self):
        """
        Restart the game with the same configuration.
        """
        self.board = self.initialize_board()
        self.is_game_over = False
        self.is_winner = False
        return "Game restarted."

    def get_cell(self, row, col):
        """
        Get the current state of the cell (for UI to query).
        Returns a tuple (is_revealed, adjacent_mines, is_mine).
        """
        cell = self.board.grid[row][col]
        return (cell.is_revealed, cell.adjacent_mines, cell.is_mine)


    def initialize_board(self):
        self.start_time = time.time()
        return Board(self.rows, self.cols, self.num_mines)


    def get_elapsed_time(self):
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0
