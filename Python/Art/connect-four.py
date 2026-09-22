"""
connect-four.py
A terminal-based Connect Four game.

Play two-player, or against the computer (which looks ahead for
immediate wins and blocks, otherwise plays a reasonable heuristic
move). Drop discs into columns; first to connect four in a row
(horizontally, vertically, or diagonally) wins.
"""

import random

ROWS = 6
COLS = 7
EMPTY = "."

def new_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def display_board(board):
    print()
    for row in board:
        print(" " + " ".join(row))
    print(" " + " ".join(str(c + 1) for c in range(COLS)))
    print()

def is_column_full(board, col):
    return board[0][col] != EMPTY

def get_valid_columns(board):
    return [c for c in range(COLS) if not is_column_full(board, c)]

def drop_disc(board, col, symbol):
    """Drop a disc into the lowest empty row of the column. Returns the row it landed in."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = symbol
            return row
    return None

def undo_drop(board, row, col):
    board[row][col] = EMPTY

def check_winner(board, symbol):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def is_board_full(board):
    return len(get_valid_columns(board)) == 0

def get_human_move(board):
    while True:
        raw = input("Choose a column (1-7): ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= COLS):
            print(f"Please enter a number from 1 to {COLS}.")
            continue
        col = int(raw) - 1
        if is_column_full(board, col):
            print("That column is full. Choose another.")
            continue
        return col

def find_winning_column(board, symbol):
    for col in get_valid_columns(board):
        row = drop_disc(board, col, symbol)
        won = check_winner(board, symbol)
        undo_drop(board, row, col)
        if won:
            return col
    return None

def get_computer_move(board, computer_symbol, human_symbol):
    col = find_winning_column(board, computer_symbol)
    if col is not None:
        return col

    col = find_winning_column(board, human_symbol)
    if col is not None:
        return col

    center = COLS // 2
    columns_by_preference = sorted(get_valid_columns(board), key=lambda c: abs(c - center))
    best_distance = abs(columns_by_preference[0] - center)
    best_columns = [c for c in columns_by_preference if abs(c - center) == best_distance]
    return random.choice(best_columns)

def choose_mode():
    print("\n1. Two players")
    print("2. Vs Computer")
    while True:
        choice = input("Choose a mode (1-2): ").strip()
        if choice in ("1", "2"):
            return choice == "2"
        print("Please enter 1 or 2.")

def choose_symbol():
    while True:
        choice = input("Do you want to be Red (R) or Yellow (Y)? Red goes first: ").strip().upper()
        if choice in ("R", "Y"):
            return choice
        print("Please enter R or Y.")

def play_game(vs_computer, human_symbol, computer_symbol):
    board = new_board()
    current_symbol = "R"

    display_board(board)

    while True:
        if vs_computer and current_symbol == computer_symbol:
            print("Computer's turn...")
            col = get_computer_move(board, computer_symbol, human_symbol)
        else:
            print(f"Player {current_symbol}'s turn.")
            col = get_human_move(board)

        drop_disc(board, col, current_symbol)
        display_board(board)

        if check_winner(board, current_symbol):
            if vs_computer:
                if current_symbol == human_symbol:
                    print("🎉 You win!")
                else:
                    print("💀 The computer wins!")
            else:
                print(f"🎉 Player {current_symbol} wins!")
            return current_symbol

        if is_board_full(board):
            print("It's a tie!")
            return None

        current_symbol = "Y" if current_symbol == "R" else "R"

def main():
    print("=" * 30)
    print("          CONNECT FOUR")
    print("=" * 30)

    scores = {"R": 0, "Y": 0, "ties": 0}

    while True:
        vs_computer = choose_mode()
        human_symbol = "R"
        computer_symbol = "Y"

        if vs_computer:
            human_symbol = choose_symbol()
            computer_symbol = "Y" if human_symbol == "R" else "R"

        winner = play_game(vs_computer, human_symbol, computer_symbol)

        if winner is None:
            scores["ties"] += 1
        else:
            scores[winner] += 1

        print(f"\nScore — Red: {scores['R']}, Yellow: {scores['Y']}, Ties: {scores['ties']}")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()