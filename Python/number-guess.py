import random

def choose_difficulty():
    print("\nChoose a difficulty:")
    print("1. Easy    (1-50,  10 guesses)")
    print("2. Medium  (1-100, 7 guesses)")
    print("3. Hard    (1-500, 9 guesses)")
    print("4. Custom")

    while True:
        choice = input("Enter 1-4: ").strip()
        if choice == "1":
            return 1, 50, 10
        elif choice == "2":
            return 1, 100, 7
        elif choice == "3":
            return 1, 500, 9
        elif choice == "4":
            return custom_difficulty()
        else:
            print("Please enter a number from 1 to 4.")

def custom_difficulty():
    low = input_int("Enter the lowest number in range: ")
    high = input_int("Enter the highest number in range: ", minimum=low + 1)
    max_guesses = input_int("How many guesses should be allowed? ", minimum=1)
    return low, high, max_guesses

def input_int(prompt, minimum=None):
    while True:
        value = input(prompt).strip()
        if not value.lstrip("-").isdigit():
            print("Please enter a whole number.")
            continue
        value = int(value)
        if minimum is not None and value < minimum:
            print(f"Please enter a number of at least {minimum}.")
            continue
        return value

def play_round(low, high, max_guesses):
    target = random.randint(low, high)
    guesses_used = 0

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {max_guesses} guesses. Good luck!\n")

    while guesses_used < max_guesses:
        remaining = max_guesses - guesses_used
        guess = input_int(f"Guess ({remaining} guess{'es' if remaining != 1 else ''} left): ",
                           minimum=None)
        guesses_used += 1

        if guess < low or guess > high:
            print(f"That's outside the range ({low}-{high}), but it still counts as a guess!")

        if guess == target:
            print(f"\n🎉 Correct! The number was {target}.")
            print(f"You got it in {guesses_used} guess{'es' if guesses_used != 1 else ''}.")
            return guesses_used

        elif guess < target:
            print("Too low.\n")
        else:
            print("Too high.\n")

    print(f"\n Out of guesses! The number was {target}.")
    return None

def main():
    print("=" * 30)
    print("     NUMBER GUESSING GAME")
    print("=" * 30)

    best_score = None

    while True:
        low, high, max_guesses = choose_difficulty()
        result = play_round(low, high, max_guesses)

        if result is not None:
            if best_score is None or result < best_score:
                best_score = result
                print("New best score this session!")
            print(f"Best score so far: {best_score} guess{'es' if best_score != 1 else ''}")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()