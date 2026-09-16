import sys
import time

player = {
    "name": "",
    "godly_parent": "",
    "inventory": [],
    "health": 100,
}

def slow_print(text, delay=0.015):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def pause():
    input("\n(press Enter to continue)")

def choose(prompt, options):
    """Display numbered options and return the chosen option string."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")

    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Please choose a valid option number.")

def intro():
    slow_print("=" * 50)
    slow_print("           CAMP HALF-BLOOD: THE LOST RELIC")
    slow_print("=" * 50)
    pause()

    player["name"] = input("\nWhat's your name, demigod? ").strip() or "Hero"

    slow_print(f"\nWelcome, {player['name']}. You've just arrived at Camp Half-Blood,")
    slow_print("sensing something is... different about you. The other campers")
    slow_print("whisper as you pass. Then, above your head, a shimmering symbol appears.")
    pause()

    parent = choose("A godly symbol flares above you. Who is your godly parent?", [
        "Poseidon (Sea, storms, earthquakes)",
        "Athena (Wisdom, strategy, warfare)",
        "Ares (War, violence, courage)",
        "Hermes (Travel, thieves, messengers)",
    ])
    player["godly_parent"] = parent.split(" ")[0]

    slow_print(f"\nA murmur runs through the crowd: 'All hail {player['name']},")
    slow_print(f"child of {player['godly_parent']}!'")
    pause()

    player["inventory"].append("bronze dagger")
    slow_print("\nChiron hands you a bronze dagger. 'You'll need this,' he says.")
    slow_print("'A relic has been stolen from Olympus. If it isn't returned by")
    slow_print("sundown in three days, the gods will blame each other, and war")
    slow_print("will break out. You must find it first.'")
    pause()

    forest_scene()

def forest_scene():
    slow_print("\n--- THE WHISPERING FOREST ---")
    slow_print("You enter the forest bordering camp. The trees seem to lean in,")
    slow_print("murmuring warnings you can't quite make out.")

    choice = choose("A path splits ahead. What do you do?", [
        "Follow the sound of running water",
        "Investigate a strange glowing light",
        "Climb a tree to get a better view",
    ])

    if choice.startswith("Follow"):
        river_scene()
    elif choice.startswith("Investigate"):
        light_scene()
    else:
        tree_scene()

def river_scene():
    slow_print("\nYou follow the sound and find a river blocking your path.")

    if player["godly_parent"] == "Poseidon":
        slow_print("The water ripples toward you, almost affectionately. You feel")
        slow_print("a pull — the river bends, forming a dry path across.")
        slow_print("You cross safely, and notice a rusted key glinting in the mud.")
        player["inventory"].append("rusted key")
        pause()
    else:
        choice = choose("The current looks strong. How do you cross?", [
            "Wade across carefully",
            "Look for a fallen log upstream",
        ])
        if choice.startswith("Wade"):
            slow_print("\nThe current is stronger than it looked. You're swept a few")
            slow_print("feet downstream before scrambling out, soaked but alive.")
            player["health"] -= 10
        else:
            slow_print("\nYou find a fallen log and cross safely, spotting a rusted")
            slow_print("key wedged in the bark on the other side.")
            player["inventory"].append("rusted key")
        pause()

    cave_scene()

def light_scene():
    slow_print("\nThe glow leads you to a small clearing where a bronze coin")
    slow_print("hovers above a stone pedestal, humming with energy.")

    choice = choose("Do you take the coin?", [
        "Take it — could be useful",
        "Leave it — feels like a trap",
    ])

    if choice.startswith("Take"):
        slow_print("\nAs your fingers close around it, the ground shakes.")
        slow_print("A hellhound bursts from the treeline!")
        combat_scene("hellhound")
        if player["health"] > 0:
            player["inventory"].append("bronze coin")
    else:
        slow_print("\nGood instinct. The pedestal crumbles to dust moments later —")
        slow_print("it was rigged to summon something nasty.")
        pause()

    cave_scene()

def tree_scene():
    slow_print("\nYou climb high and spot a cave entrance to the west, glowing")
    slow_print("faintly with a strange orange light.")
    slow_print("You also notice a coiled shape near the cave — could be a monster.")
    pause()
    cave_scene()

def combat_scene(monster_name):
    monster_health = 40
    slow_print(f"\n  A {monster_name} attacks!")

    while monster_health > 0 and player["health"] > 0:
        action = choose("What do you do?", [
            "Attack with your dagger",
            "Try to dodge and look for an opening",
            "Use an item" if player["inventory"] else "Attack with your dagger",
        ])

        if action.startswith("Attack"):
            damage = 15
            monster_health -= damage
            slow_print(f"You strike the {monster_name} for {damage} damage!")
        elif action.startswith("Try"):
            slow_print("You dodge nimbly, but land no hit this turn.")
        elif action.startswith("Use"):
            slow_print(f"\nInventory: {', '.join(player['inventory'])}")
            slow_print("(Items are for later — for now, this just costs you a turn.)")

        if monster_health > 0:
            damage_taken = 12
            player["health"] -= damage_taken
            slow_print(f"The {monster_name} bites back for {damage_taken} damage!")
            slow_print(f"Your health: {player['health']} | {monster_name}'s health: {max(monster_health, 0)}")

    if player["health"] <= 0:
        game_over()
    else:
        slow_print(f"\nYou defeated the {monster_name}!")
        pause()

def cave_scene():
    slow_print("\n--- THE GLOWING CAVE ---")
    slow_print("Inside, the walls pulse with faint orange light. At the center,")
    slow_print("on a stone altar, sits a small case radiating power.")
    slow_print("This must be the stolen relic.")

    if "rusted key" in player["inventory"]:
        slow_print("\nThe case is locked, but your rusted key fits perfectly.")
        pause()
        ending_good()
    elif "bronze coin" in player["inventory"]:
        slow_print("\nThe bronze coin in your pocket hums, and the case's lock")
        slow_print("clicks open on its own, resonating with the coin's magic.")
        pause()
        ending_good()
    else:
        choice = choose("You have no way to unlock it. What do you do?", [
            "Try to force it open",
            "Search the cave for another way",
        ])
        if choice.startswith("Try"):
            slow_print("\nThe case shocks you violently as you try to force it.")
            player["health"] -= 30
            if player["health"] <= 0:
                game_over()
            else:
                slow_print("You stumble back, singed but alive. The relic stays sealed.")
                ending_neutral()
        else:
            slow_print("\nYou search but find nothing useful. Time is running out...")
            ending_neutral()

def ending_good():
    slow_print("\n" + "=" * 50)
    slow_print("You return to camp just as the sun dips below the hills,")
    slow_print(f"relic in hand. Chiron nods approvingly. '{player['name']},'")
    slow_print("he says, 'Olympus owes you a debt today.'")
    slow_print("\n QUEST COMPLETE — YOU SAVED OLYMPUS")
    slow_print("=" * 50)

def ending_neutral():
    slow_print("\n" + "=" * 50)
    slow_print("You return to camp empty-handed, but alive. Chiron sighs.")
    slow_print("'We'll find another way,' he says, though his eyes betray worry.")
    slow_print("\n  QUEST INCOMPLETE — THE GODS GROW RESTLESS")
    slow_print("=" * 50)

def game_over():
    slow_print("\n" + "=" * 50)
    slow_print(f"{player['name']}'s quest ends here. The Underworld awaits.")
    slow_print("\n GAME OVER")
    slow_print("=" * 50)
    sys.exit(0)

def main():
    intro()

    print("\nThanks for playing!")
    play_again = input("Play again? (y/n): ").strip().lower()
    if play_again == "y":
        player["inventory"].clear()
        player["health"] = 100
        main()

if __name__ == "__main__":
    main()