"""
battleship.py
A terminal-based Battleship game — you vs. the computer.

Place your fleet (or auto-place it), then take turns firing at
coordinates trying to sink the computer's hidden fleet before it
sinks yours. The computer uses simple hunt-and-target AI: it fires
randomly until it scores a hit, then focuses on nearby cells.
"""

import random

BOARD_SIZE = 10
SHIPS = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2),
]

EMPTY, SHIP, HIT, MISS = ".", "S", "X", "O"

def new_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def in_bounds(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def get_ship_cells(row, col, length, horizontal):
    if horizontal:
        return [(row, col + i) for i in range(length)]
    return [(row + i, col) for i in range(length)]

def can_place(board, row, col, length, horizontal):
    cells = get_ship_cells(row, col, length, horizontal)
    for r, c in cells:
        if not in_bounds(r, c) or board[r][c] != EMPTY:
            return False
    return True

def place_ship(board, row, col, length, horizontal):
    for r, c in get_ship_cells(row, col, length, horizontal):
        board[r][c] = SHIP

def auto_place_fleet(board):
    for name, length in SHIPS:
        placed = False
        while not placed:
            horizontal = random.choice([True, False])
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if can_place(board, row, col, length, horizontal):
                place_ship(board, row, col, length, horizontal)
                placed = True

def parse_coordinate(raw):
    """Parse input like 'B5' into (row, col), or return None if invalid."""
    raw = raw.strip().upper()
    if len(raw) < 2:
        return None

    col_letter = raw[0]
    row_part = raw[1:]

    if not col_letter.isalpha() or not row_part.isdigit():
        return None

    col = ord(col_letter) - ord("A")
    row = int(row_part) - 1

    if not in_bounds(row, col):
        return None

    return row, col

def manual_place_fleet(board):
    print("\nPlace your fleet. Enter a starting coordinate (e.g. 'B5') and")
    print("orientation (h = horizontal, v = vertical) for each ship.")

    for name, length in SHIPS:
        while True:
            print_board(board, hide_ships=False, label="Your fleet")
            print(f"Placing {name} (length {length})")
            coord_raw = input("Starting coordinate: ").strip()
            coord = parse_coordinate(coord_raw)
            if coord is None:
                print("Invalid coordinate. Use format like 'B5'.")
                continue

            orientation = input("Orientation (h/v): ").strip().lower()
            if orientation not in ("h", "v"):
                print("Please enter 'h' or 'v'.")
                continue

            row, col = coord
            horizontal = orientation == "h"

            if can_place(board, row, col, length, horizontal):
                place_ship(board, row, col, length, horizontal)
                break
            else:
                print("Can't place there — it's off the board or overlaps another ship.")

def print_board(board, hide_ships, label=""):
    if label:
        print(f"\n{label}")

    col_header = "   " + " ".join(chr(ord("A") + c) for c in range(BOARD_SIZE))
    print(col_header)

    for r in range(BOARD_SIZE):
        row_display = []
        for c in range(BOARD_SIZE):
            cell = board[r][c]
            if hide_ships and cell == SHIP:
                row_display.append(EMPTY)
            else:
                row_display.append(cell)
        print(f"{r + 1:2} " + " ".join(row_display))

def all_ships_sunk(board):
    return not any(SHIP in row for row in board)

def fire_at(board, row, col):
    """Apply a shot to board. Returns 'hit', 'miss', or 'repeat'."""
    cell = board[row][col]
    if cell in (HIT, MISS):
        return "repeat"
    if cell == SHIP:
        board[row][col] = HIT
        return "hit"
    board[row][col] = MISS
    return "miss"

def get_player_shot(shots_board):
    while True:
        raw = input("\nFire at (e.g. 'B5'): ").strip()
        coord = parse_coordinate(raw)
        if coord is None:
            print("Invalid coordinate. Use format like 'B5'.")
            continue
        row, col = coord
        if shots_board[row][col] in (HIT, MISS):
            print("You already fired there.")
            continue
        return row, col

class ComputerAI:
    """Hunt-and-target AI: fires randomly until a hit, then targets neighbors."""

    def __init__(self):
        self.target_queue = []
        self.tried = set()

    def get_shot(self):
        while self.target_queue:
            row, col = self.target_queue.pop(0)
            if (row, col) not in self.tried and in_bounds(row, col):
                return row, col

        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if (row, col) not in self.tried:
                return row, col

    def report_result(self, row, col, result):
        self.tried.add((row, col))
        if result == "hit":
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                neighbor = (row + dr, col + dc)
                if neighbor not in self.tried:
                    self.target_queue.append(neighbor)

def player_turn(computer_board):
    row, col = get_player_shot(computer_board)
    result = fire_at(computer_board, row, col)
    coord_str = f"{chr(ord('A') + col)}{row + 1}"

    if result == "hit":
        print(f"Hit at {coord_str}!")
    else:
        print(f"Miss at {coord_str}.")

    return result

def computer_turn(player_board, ai):
    row, col = ai.get_shot()
    result = fire_at(player_board, row, col)
    ai.report_result(row, col, result)
    coord_str = f"{chr(ord('A') + col)}{row + 1}"

    if result == "hit":
        print(f"Computer fires at {coord_str}... Hit!")
    else:
        print(f"Computer fires at {coord_str}... Miss.")

    return result

def choose_placement_mode():
    print("\nHow do you want to place your fleet?")
    print("1. Auto-place (random)")
    print("2. Manual placement")
    while True:
        choice = input("Choose 1-2: ").strip()
        if choice in ("1", "2"):
            return choice == "2"
        print("Please enter 1 or 2.")

def play_game():
    player_board = new_board()
    computer_board = new_board()

    if choose_placement_mode():
        manual_place_fleet(player_board)
    else:
        auto_place_fleet(player_board)
        print("Your fleet has been placed automatically.")

    auto_place_fleet(computer_board)
    ai = ComputerAI()

    while True:
        print_board(player_board, hide_ships=False, label="Your fleet")
        print_board(computer_board, hide_ships=True, label="Enemy waters")

        player_turn(computer_board)
        if all_ships_sunk(computer_board):
            print("\n You sank the entire enemy fleet! You win!")
            return

        computer_turn(player_board, ai)
        if all_ships_sunk(player_board):
            print_board(player_board, hide_ships=False, label="Your fleet")
            print("\n Your fleet has been destroyed. Computer wins!")
            return

def main():
    print("=" * 30)
    print("          BATTLESHIP")
    print("=" * 30)

    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()