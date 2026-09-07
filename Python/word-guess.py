import random

WORD_BANK = {
    "animals": ["elephant", "giraffe", "penguin", "dolphin", "kangaroo", "octopus"],
    "programming": ["python", "variable", "function", "iterate", "boolean", "recursion"],
    "countries": ["canada", "brazil", "japan", "germany", "egypt", "australia"],
    "food": ["spaghetti", "avocado", "pancake", "burrito", "sandwich", "pineapple"],
}

MAX_WRONG_GUESSES = 6

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    ---------
    """,
]

def choose_category():
    print("\nChoose a category:")
    categories = list(WORD_BANK.keys())
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.title()}")
    print(f"{len(categories) + 1}. Random")

    while True:
        choice = input(f"Enter 1-{len(categories) + 1}: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            elif choice == len(categories) + 1:
                return random.choice(categories)
        print("Please enter a valid option.")

def get_display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def play_round(category):
    word = random.choice(WORD_BANK[category]).lower()
    guessed_letters = set()
    wrong_guesses = 0

    print(f"\nCategory: {category.title()}")
    print(f"The word has {len(word)} letters. You have {MAX_WRONG_GUESSES} wrong guesses allowed.\n")

    while wrong_guesses < MAX_WRONG_GUESSES:
        print(HANGMAN_STAGES[wrong_guesses])
        print(get_display_word(word, guessed_letters))

        if guessed_letters:
            wrong_so_far = sorted(guessed_letters - set(word))
            if wrong_so_far:
                print(f"Wrong guesses: {', '.join(wrong_so_far)}")

        if all(letter in guessed_letters for letter in word):
            print(f"\n🎉 You got it! The word was '{word}'.")
            return True

        guess = input("\nGuess a letter (or the whole word): ").strip().lower()

        if not guess:
            print("Please enter something.")
            continue

        if len(guess) > 1:
            if guess == word:
                guessed_letters.update(word)
                print(f"\n Correct! The word was '{word}'.")
                return True
            else:
                print("That's not the word.")
                wrong_guesses += 1
                continue

        if not guess.isalpha():
            print("Please enter a letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess not in word:
            wrong_guesses += 1
            print(f"'{guess}' is not in the word.")
        else:
            print(f"Nice, '{guess}' is in the word!")

    print(HANGMAN_STAGES[MAX_WRONG_GUESSES])
    print(f"\n Out of guesses! The word was '{word}'.")
    return False

def main():
    print("=" * 30)
    print("      WORD GUESSING GAME")
    print("=" * 30)

    wins = 0
    losses = 0

    while True:
        category = choose_category()
        won = play_round(category)

        if won:
            wins += 1
        else:
            losses += 1

        print(f"\nScore: {wins} win{'s' if wins != 1 else ''}, {losses} loss{'es' if losses != 1 else ''}")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()