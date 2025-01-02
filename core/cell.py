class Cell:
    def __init__(self):
        """
        Initialize a cell with default values.
        """
        self.is_mine = False         # True if the cell contains a mine
        self.is_flagged = False      # True if the cell is flagged by the player
        self.is_revealed = False     # True if the cell has been revealed
        self.is_clear = False        # True if the cell is not a mine with no adjacent mines
        self.adjacent_mines = 0      # Number of mines in neighboring cells

    def reveal(self):
        """
        Reveal the cell if it is not flagged.
        Returns True if successfully revealed, False otherwise.
        """
        if not self.is_flagged:
            self.is_revealed = True
            return True
        return False

    def toggle_flag(self):
        """
        Toggle the flagged state of the cell.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def __str__(self):
        """
        String representation of the cell for debugging or display purposes.
        """
        if self.is_flagged:
            return "F"  # Flagged
        if not self.is_revealed:
            return "?"  # Hidden
        if self.is_mine:
            return "*"  # Mine
        if self.is_revealed and self.adjacent_mines == 0:
            return " "  # Blank if no adjacent mines
        return str(self.adjacent_mines)  # Number of adjacent mines if revealed
