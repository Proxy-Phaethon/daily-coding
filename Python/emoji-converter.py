import sys

try:
    import emoji
except ImportError:
    print("This tool requires the 'emoji' package. Install it with:")
    print("    pip install emoji --break-system-packages")
    sys.exit(1)

def emojis_to_text(text):
    """Replace emoji characters with their :shortcode: text equivalent."""
    return emoji.demojize(text)

def text_to_emojis(text):
    """Replace :shortcode: text with the actual emoji character."""
    return emoji.emojize(text)

def find_emojis(text):
    """Return a list of (emoji_char, shortcode) pairs found in the text."""
    results = []
    for item in emoji.emoji_list(text):
        char = item["emoji"]
        shortcode = emoji.demojize(char)
        results.append((char, shortcode))
    return results

def show_menu():
    print("\n" + "=" * 40)
    print("        EMOJI <-> TEXT CONVERTER")
    print("=" * 40)
    print("1. Convert emojis to text (😀 -> :grinning_face:)")
    print("2. Convert text to emojis (:grinning_face: -> 😀)")
    print("3. List emojis found in a message")
    print("4. Exit")

def handle_emojis_to_text():
    text = input("\nEnter text containing emojis: ")
    converted = emojis_to_text(text)
    print(f"\nResult: {converted}")

def handle_text_to_emojis():
    print("\nEnter text using :shortcode: format (e.g. 'I feel :fire: today')")
    text = input("Text: ")
    converted = text_to_emojis(text)
    print(f"\nResult: {converted}")

def handle_list_emojis():
    text = input("\nEnter a message: ")
    found = find_emojis(text)

    if not found:
        print("No emojis found in that message.")
        return

    print(f"\nFound {len(found)} emoji(s):")
    for char, shortcode in found:
        print(f"  {char}  ->  {shortcode}")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            handle_emojis_to_text()
        elif choice == "2":
            handle_text_to_emojis()
        elif choice == "3":
            handle_list_emojis()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()