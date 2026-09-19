"""
minesweeper.py
A terminal-based Minesweeper game.

Reveal cells without hitting a mine. Numbers show how many mines are
adjacent to that cell. Flag cells you suspect are mines. Clearing
every non-mine cell wins the game.
"""

import random

DIFFICULTIES = {
    "1": ("Easy", 9, 9, 10),
    "2": ("Medium", 16, 16, 40),
    "3": ("Hard", 16, 30, 99),
}

def create_board(rows, cols, num_mines):
    """Return a fresh board (mines placed, no cells revealed yet)."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]

    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    mine_positions = set(random.sample(all_positions, num_mines))

    for r, c in mine_positions:
        board[r][c] = "*"

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "*":
                continue
            board[r][c] = count_adjacent_mines(board, r, c, rows, cols)

    return board, mine_positions

def count_adjacent_mines(board, row, col, rows, cols):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "*":
                count += 1
    return count

def new_revealed_grid(rows, cols):
    return [[False for _ in range(cols)] for _ in range(rows)]

def new_flagged_grid(rows, cols):
    return [[False for _ in range(cols)] for _ in range(rows)]

def reveal_cell(board, revealed, flagged, row, col, rows, cols):
    """Reveal a cell, flood-filling outward if it's a 0 (no adjacent mines)."""
    if revealed[row][col] or flagged[row][col]:
        return

    revealed[row][col] = True

    if board[row][col] == 0:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and not revealed[nr][nc]:
                    reveal_cell(board, revealed, flagged, nr, nc, rows, cols)

def display_board(board, revealed, flagged, rows, cols, reveal_all=False):
    col_header = "    " + " ".join(f"{c:2}" for c in range(cols))
    print(col_header)
    print("   " + "---" * cols)

    for r in range(rows):
        row_cells = []
        for c in range(cols):
            if reveal_all and board[r][c] == "*":
                row_cells.append(" *")
            elif flagged[r][c] and not revealed[r][c]:
                row_cells.append(" F")
            elif not revealed[r][c]:
                row_cells.append(" .")
            elif board[r][c] == "*":
                row_cells.append(" *")
            elif board[r][c] == 0:
                row_cells.append("  ")
            else:
                row_cells.append(f" {board[r][c]}")
        print(f"{r:2} |" + "".join(row_cells))
    print()

def count_unrevealed_safe_cells(board, revealed, rows, cols):
    count = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != "*" and not revealed[r][c]:
                count += 1
    return count

def get_input(rows, cols):
    print("Enter a move as: <row> <col> <r/f>   (r = reveal, f = flag/unflag)")
    print("Example: 3 4 r")

    while True:
        raw = input("> ").strip().lower().split()
        if len(raw) != 3:
            print("Please enter three values: row, column, and r or f.")
            continue

        row_str, col_str, action = raw
        if not row_str.isdigit() or not col_str.isdigit():
            print("Row and column must be numbers.")
            continue

        row, col = int(row_str), int(col_str)
        if not (0 <= row < rows and 0 <= col < cols):
            print(f"Row must be 0-{rows - 1} and column must be 0-{cols - 1}.")
            continue

        if action not in ("r", "f"):
            print("Action must be 'r' (reveal) or 'f' (flag).")
            continue

        return row, col, action

def choose_difficulty():
    print("\nChoose a difficulty:")
    for key, (name, rows, cols, mines) in DIFFICULTIES.items():
        print(f"  {key}. {name} ({rows}x{cols}, {mines} mines)")

    while True:
        choice = input("Enter 1-3: ").strip()
        if choice in DIFFICULTIES:
            _, rows, cols, mines = DIFFICULTIES[choice]
            return rows, cols, mines
        print("Please enter 1, 2, or 3.")

def play_game():
    rows, cols, num_mines = choose_difficulty()
    board, mine_positions = create_board(rows, cols, num_mines)
    revealed = new_revealed_grid(rows, cols)
    flagged = new_flagged_grid(rows, cols)

    while True:
        display_board(board, revealed, flagged, rows, cols)
        row, col, action = get_input(rows, cols)

        if action == "f":
            flagged[row][col] = not flagged[row][col]
            continue

        # action == "r"
        if flagged[row][col]:
            print("That cell is flagged. Unflag it first if you want to reveal it.")
            continue

        if board[row][col] == "*":
            display_board(board, revealed, flagged, rows, cols, reveal_all=True)
            print("BOOM! You hit a mine. Game over.")
            return False

        reveal_cell(board, revealed, flagged, row, col, rows, cols)

        if count_unrevealed_safe_cells(board, revealed, rows, cols) == 0:
            display_board(board, revealed, flagged, rows, cols, reveal_all=True)
            print("You cleared the board! You win!")
            return True

def main():
    print("=" * 30)
    print("          MINESWEEPER")
    print("=" * 30)

    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()