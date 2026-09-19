"""
tic-tac-toe.py
A terminal-based Tic-Tac-Toe game.

Play against a friend (two-player) or against the computer, which
plays using basic strategy: win if possible, block if necessary,
otherwise pick a reasonable spot.
"""

import random

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def new_board():
    return [" "] * 9

def display_board(board):
    def cell(i):
        return board[i] if board[i] != " " else str(i + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()

def get_winner(board):
    for a, b, c in WINNING_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    return " " not in board

def get_empty_cells(board):
    return [i for i in range(9) if board[i] == " "]

def get_human_move(board):
    while True:
        raw = input("Choose a cell (1-9): ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= 9):
            print("Please enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if board[index] != " ":
            print("That cell is already taken.")
            continue
        return index

def find_winning_move(board, symbol):
    for i in get_empty_cells(board):
        board[i] = symbol
        if get_winner(board) == symbol:
            board[i] = " "
            return i
        board[i] = " "
    return None

def get_computer_move(board, computer_symbol, human_symbol):
    # 1. Win if possible
    move = find_winning_move(board, computer_symbol)
    if move is not None:
        return move

    # 2. Block the human's winning move
    move = find_winning_move(board, human_symbol)
    if move is not None:
        return move

    # 3. Take the center if available
    if board[4] == " ":
        return 4

    # 4. Take a corner if available
    corners = [i for i in (0, 2, 6, 8) if board[i] == " "]
    if corners:
        return random.choice(corners)

    # 5. Otherwise take any remaining cell
    return random.choice(get_empty_cells(board))

def play_game(vs_computer, human_symbol, computer_symbol):
    board = new_board()
    current_symbol = "X"  # X always goes first

    display_board(board)

    while True:
        if vs_computer and current_symbol == computer_symbol:
            print("Computer's turn...")
            move = get_computer_move(board, computer_symbol, human_symbol)
        else:
            print(f"Player {current_symbol}'s turn.")
            move = get_human_move(board)

        board[move] = current_symbol
        display_board(board)

        winner = get_winner(board)
        if winner is not None:
            if vs_computer:
                if winner == human_symbol:
                    print("You win!")
                else:
                    print("The computer wins!")
            else:
                print(f"Player {winner} wins!")
            return winner

        if is_full(board):
            print("It's a tie!")
            return None

        current_symbol = "O" if current_symbol == "X" else "X"

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
        choice = input("Do you want to be X or O? (X goes first): ").strip().upper()
        if choice in ("X", "O"):
            return choice
        print("Please enter X or O.")

def main():
    print("=" * 30)
    print("          TIC-TAC-TOE")
    print("=" * 30)

    scores = {"X": 0, "O": 0, "ties": 0}

    while True:
        vs_computer = choose_mode()
        human_symbol = "X"
        computer_symbol = "O"

        if vs_computer:
            human_symbol = choose_symbol()
            computer_symbol = "O" if human_symbol == "X" else "X"

        winner = play_game(vs_computer, human_symbol, computer_symbol)

        if winner is None:
            scores["ties"] += 1
        else:
            scores[winner] += 1

        print(f"\nScore — X: {scores['X']}, O: {scores['O']}, Ties: {scores['ties']}")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()