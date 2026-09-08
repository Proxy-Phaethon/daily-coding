import random

CHOICES = ["rock", "paper", "scissors"]

BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}

def get_player_choice():
    while True:
        raw = input("Choose rock, paper, or scissors (r/p/s): ").strip().lower()
        if raw in CHOICES:
            return raw
        if raw in SHORTCUTS:
            return SHORTCUTS[raw]
        print("Please enter rock, paper, scissors (or r/p/s).")

def get_computer_choice():
    return random.choice(CHOICES)

def decide_winner(player, computer):
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "player"
    return "computer"

def choose_rounds():
    while True:
        raw = input("How many rounds should this match be (best of)? ").strip()
        if raw.isdigit() and int(raw) > 0:
            n = int(raw)
            if n % 2 == 0:
                print("Tip: an odd number avoids a tied match, but even works too.")
            return n
        print("Please enter a positive whole number.")

def play_match():
    total_rounds = choose_rounds()
    wins_needed = total_rounds // 2 + 1

    player_score = 0
    computer_score = 0
    round_number = 1

    print(f"\nFirst to {wins_needed} wins takes the match!\n")

    while player_score < wins_needed and computer_score < wins_needed:
        print(f"--- Round {round_number} ---")
        player = get_player_choice()
        computer = get_computer_choice()

        print(f"You chose {player}. Computer chose {computer}.")

        result = decide_winner(player, computer)

        if result == "tie":
            print("It's a tie!")
        elif result == "player":
            print("You win this round!")
            player_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1

        print(f"Score: You {player_score} - {computer_score} Computer\n")
        round_number += 1

    if player_score > computer_score:
        print(" You won the match!")
    else:
        print(" Computer won the match!")


def main():
    print("=" * 30)
    print("     ROCK, PAPER, SCISSORS")
    print("=" * 30)

    while True:
        play_match()

        again = input("\nPlay another match? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()