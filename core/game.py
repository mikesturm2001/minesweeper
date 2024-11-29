from core.board import Board

class Game:
    def __init__(self, rows, cols, num_mines):
        """
        Initialize a new game.
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = Board(rows, cols, num_mines)  # Create the board
        self.is_game_over = False
        self.is_winner = False

    def reveal_cell(self, row, col):
        """
        Handles the logic for revealing a cell.
        """
        if self.is_game_over:
            print("The game is over! Start a new game.")
            return

        cell = self.board.grid[row][col]
        if cell.is_flagged:
            print("Cell is flagged. Unflag it first to reveal.")
            return

        if cell.is_mine:
            self.is_game_over = True
            print("You hit a mine! Game over.")
        else:
            # Update the board and reveal adjacent cells if this cell is empty
            self.board.reveal_cell(row, col)

            # Check if the player has won
            self.check_win_condition()

    def flag_cell(self, row, col):
        """
        Toggles a flag on a cell.
        """
        if self.is_game_over:
            print("The game is over! Start a new game.")
            return

        cell = self.board.grid[row][col]
        cell.toggle_flag()

    def check_win_condition(self):
        """
        Check if all non-mine cells have been revealed.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board.grid[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return  # Still cells to uncover, no win yet

        # If we reach here, the player has revealed all non-mine cells
        self.is_game_over = True
        self.is_winner = True
        print("Congratulations! You've won the game.")

    def restart(self):
        """
        Restart the game with the same configuration.
        """
        self.board = Board(self.rows, self.cols, self.num_mines)
        self.is_game_over = False
        self.is_winner = False