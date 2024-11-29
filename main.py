from core.game import Game

def main():
    print("Welcome to Minesweeper!")

    while True:
        try:
            rows = int(input("Enter the number of rows: "))
            cols = int(input("Enter the number of columns: "))
            num_mines = int(input("Enter the number of mines: "))
            break  # Exit the loop if everything is valid
        except ValueError:
            print("Please enter valid integers for rows, columns, and mines.")

    # Create the minesweeper game
    game = Game(rows, cols, num_mines)

    # Main game loop
    while not game.is_game_over:
        print(game.board)  # Add a __str__() method to the Board class for visualization
        action = input("Enter action (r row col to reveal, f row col to flag): ").strip()

        # Parse user input
        parts = action.split()
        if len(parts) != 3:
            print("Invalid input format! Use 'r row col' to reveal or 'f row col' to flag.")
            continue

        command, row, col = parts[0], int(parts[1]), int(parts[2])

        # Handle commands
        if command == "r":  # Reveal cell
            game.reveal_cell(row, col)
        elif command == "f":  # Flag cell
            game.flag_cell(row, col)
        else:
            print("Invalid command! Use 'r' to reveal or 'f' to flag.")

    # End of game
    if game.is_winner:
        print("Congratulations, you won!")
    else:
        print("You hit a mine! Game over.")

# Ensure script runs as the main entry point
if __name__ == "__main__":
    main()