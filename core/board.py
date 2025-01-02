import random
from collections import deque
from core.cell import Cell


class Board:
    def __init__(self, rows, cols, num_mines):
        """
        Initializes a new Minesweeper board with the given number of rows, columns, and mines.
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]  # Create a grid of cells
        self._place_mines()  # Place the mines randomly
        self.calculate_adjacent_mines()  # Calculate adjacent mines for all cells

    def _place_mines(self):
        """
        Randomly places mines on the board.
        """
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.grid[row][col].is_mine:  # Ensure no duplicate mine placement
                self.grid[row][col].is_mine = True
                mines_placed += 1

    def calculate_adjacent_mines(self):
        """
        Calculates the number of mines adjacent to each non-mine cell.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.grid[row][col].is_mine:
                    self.grid[row][col].adjacent_mines = self._count_adjacent_mines(row, col)

    def _count_adjacent_mines(self, row, col):
        """
        Counts how many mines are adjacent to the given cell.
        """

        # Create a list of tuples to navigate surrounding cells
        adjacent_positions = [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1),          (0, 1),
                              (1, -1), (1, 0), (1, 1)]
        mine_count = 0
        for row_offset, column_offset in adjacent_positions:
            surrounding_row, surrounding_column = row + row_offset, col + column_offset
            if self.is_valid_position(surrounding_row, surrounding_column):
                if self.grid[surrounding_row][surrounding_column].is_mine:
                    mine_count += 1
        return mine_count

    # Depth first search implementation of reveal_cell
    #
    # def reveal_cell(self, row, col):
    #     """
    #     Reveals a specific cell and propagates the reveal if the cell has no adjacent mines.
    #     """
    #     if not self.is_valid_position(row, col) or self.grid[row][col].is_revealed:
    #         return False  # Invalid position or already revealed
    #
    #     cell = self.grid[row][col]
    #     cell.reveal()  # Reveal the cell
    #
    #     # Create a list of tuples to navigate surrounding cells
    #     adjacent_positions = [(-1, -1), (-1, 0), (-1, 1),
    #                           (0, -1),          (0, 1),
    #                           (1, -1), (1, 0), (1, 1)]
    #
    #     # If there are no adjacent mines, reveal neighboring cells recursively
    #     if cell.adjacent_mines == 0:
    #         for dr, dc in adjacent_positions:
    #             new_row, new_col = row + dr, col + dc
    #             if self.is_valid_position(new_row, new_col) and not self.grid[new_row][new_col].is_revealed:
    #                 self.reveal_cell(new_row, new_col)
    #
    #     return True

    # Breadth first search of reveal cell
    def reveal_cell(self, row, col):
        """
        Reveals a specific cell and propagates the reveal using breadth-first search
        if the cell has no adjacent mines.
        """
        if not self.is_valid_position(row, col) or self.grid[row][col].is_revealed:
            return False  # Invalid position or already revealed

        # Create a queue to manage cells to process
        queue = deque()
        queue.append((row, col))  # Start with the given cell

        # Create a list of tuples to navigate surrounding cells
        adjacent_positions = [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1), (0, 1),
                              (1, -1), (1, 0), (1, 1)]

        while queue:
            current_row, current_col = queue.popleft()  # Pop the next cell from the queue
            current_cell = self.grid[current_row][current_col]

            # Skip if already revealed (this can happen with multiple queue additions)
            if current_cell.is_revealed:
                continue

            # Reveal the current cell
            current_cell.reveal()

            # If the current cell has no adjacent mines, add its neighbors to the queue
            if current_cell.adjacent_mines == 0:
                for dr, dc in adjacent_positions:
                    new_row, new_col = current_row + dr, current_col + dc
                    if self.is_valid_position(new_row, new_col):
                        neighbor_cell = self.grid[new_row][new_col]
                        if not neighbor_cell.is_revealed and (new_row, new_col) not in queue:
                            queue.append((new_row, new_col))  # Add to queue for processing

        return True

    def is_valid_position(self, row, col):
        """
        Checks if the given position is within the bounds of the board.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __str__(self):
        """
        String representation of the board for debugging or display purposes.
        """
        row_count = 0

        # Generate the numbers leading up to `col`
        columns = list(range(self.cols))
        board_str = f"  {' '.join(str(col) for col in columns)}\n"
        for row in self.grid:
            board_str += str(row_count) + " "
            row_count += 1
            for cell in row:
                board_str += str(cell) + " "
            board_str += "\n"
        return board_str
