"""
garden-sim.py
A text-based garden simulator.

Plant seeds, water your plots, watch crops grow over in-game days,
harvest them, and sell your harvest for coins to buy more seeds.
Progress is saved to a JSON file, so you can pick up where you left
off across multiple play sessions.
"""

import json
import os
import random

SAVE_FILE = "garden_save.json"
NUM_PLOTS = 6

CROPS = {
    "carrot": {"grow_days": 3, "seed_cost": 5, "sell_price": 10, "emoji": "🥕"},
    "tomato": {"grow_days": 5, "seed_cost": 10, "sell_price": 22, "emoji": "🍅"},
    "pumpkin": {"grow_days": 8, "seed_cost": 20, "sell_price": 50, "emoji": "🎃"},
}

def new_game_state():
    return {
        "day": 1,
        "coins": 30,
        "seeds": {"carrot": 3, "tomato": 0, "pumpkin": 0},
        "harvest": {"carrot": 0, "tomato": 0, "pumpkin": 0},
        "plots": [None] * NUM_PLOTS,  # each plot: None, or {"crop", "days_grown", "watered_today"}
    }

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No save file found. Starting a new garden!")
        return new_game_state()

    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("Save file was corrupted. Starting a new garden.")
        return new_game_state()

def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def display_garden(state):
    print(f"\n Day {state['day']}    Coins: {state['coins']}")
    print("-" * 40)
    print("Your plots:")

    for i, plot in enumerate(state["plots"], start=1):
        if plot is None:
            print(f"  Plot {i}: (empty)")
        else:
            crop = plot["crop"]
            info = CROPS[crop]
            watered = "💧" if plot["watered_today"] else "  "
            if plot["days_grown"] >= info["grow_days"]:
                status = " Ready to harvest!"
            else:
                status = f"growing ({plot['days_grown']}/{info['grow_days']} days)"
            print(f"  Plot {i}: {info['emoji']} {crop} {watered} - {status}")

    print("\nSeeds:  " + ", ".join(f"{c}: {n}" for c, n in state["seeds"].items()))
    print("Harvest:" + " " + ", ".join(f"{c}: {n}" for c, n in state["harvest"].items()))

def plant_seed(state):
    empty_plots = [i for i, p in enumerate(state["plots"]) if p is None]
    if not empty_plots:
        print("All your plots are full!")
        return

    available_seeds = {c: n for c, n in state["seeds"].items() if n > 0}
    if not available_seeds:
        print("You don't have any seeds. Buy some first!")
        return

    print("\nWhich crop do you want to plant?")
    crop_list = list(available_seeds.keys())
    for i, crop in enumerate(crop_list, start=1):
        print(f"  {i}. {crop} (you have {available_seeds[crop]} seeds)")

    choice = input(f"Choose 1-{len(crop_list)}: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(crop_list)):
        print("Invalid choice.")
        return
    crop = crop_list[int(choice) - 1]

    print(f"\nEmpty plots: {[i + 1 for i in empty_plots]}")
    plot_choice = input("Which plot number? ").strip()
    if not plot_choice.isdigit() or (int(plot_choice) - 1) not in empty_plots:
        print("Invalid plot.")
        return

    plot_index = int(plot_choice) - 1
    state["plots"][plot_index] = {"crop": crop, "days_grown": 0, "watered_today": False}
    state["seeds"][crop] -= 1
    print(f"Planted {crop} in plot {plot_index + 1}.")

def water_plots(state):
    watered_any = False
    for plot in state["plots"]:
        if plot is not None and not plot["watered_today"]:
            plot["watered_today"] = True
            watered_any = True

    if watered_any:
        print("You watered all your growing plots. They'll grow faster today!")
    else:
        print("Nothing needed watering.")

def harvest_crops(state):
    harvested_any = False
    for i, plot in enumerate(state["plots"]):
        if plot is not None:
            info = CROPS[plot["crop"]]
            if plot["days_grown"] >= info["grow_days"]:
                state["harvest"][plot["crop"]] += 1
                print(f"Harvested {plot['crop']} from plot {i + 1}!")
                state["plots"][i] = None
                harvested_any = True

    if not harvested_any:
        print("Nothing is ready to harvest yet.")

def sell_harvest(state):
    total_value = sum(CROPS[c]["sell_price"] * n for c, n in state["harvest"].items())
    if total_value == 0:
        print("You have no harvest to sell.")
        return

    print(f"\nSelling all harvest for {total_value} coins:")
    for crop, count in state["harvest"].items():
        if count > 0:
            print(f"  {count}x {crop} @ {CROPS[crop]['sell_price']} coins each")

    confirm = input("Confirm sale? (y/n): ").strip().lower()
    if confirm == "y":
        state["coins"] += total_value
        for crop in state["harvest"]:
            state["harvest"][crop] = 0
        print(f"Sold! You now have {state['coins']} coins.")
    else:
        print("Cancelled.")

def buy_seeds(state):
    print("\nSeed shop:")
    crop_list = list(CROPS.keys())
    for i, crop in enumerate(crop_list, start=1):
        info = CROPS[crop]
        print(f"  {i}. {crop} - {info['seed_cost']} coins (grows in {info['grow_days']} days, sells for {info['sell_price']})")

    choice = input(f"Buy which seed? (1-{len(crop_list)}, or 'q' to cancel): ").strip()
    if choice.lower() == "q":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(crop_list)):
        print("Invalid choice.")
        return

    crop = crop_list[int(choice) - 1]
    cost = CROPS[crop]["seed_cost"]

    qty_input = input("How many? ").strip()
    quantity = int(qty_input) if qty_input.isdigit() else 1

    total_cost = cost * quantity
    if total_cost > state["coins"]:
        print(f"Not enough coins. You need {total_cost}, but have {state['coins']}.")
        return

    state["coins"] -= total_cost
    state["seeds"][crop] += quantity
    print(f"Bought {quantity}x {crop} seed(s) for {total_cost} coins.")

def advance_day(state):
    for plot in state["plots"]:
        if plot is not None:
            growth = 2 if plot["watered_today"] else 1
            plot["days_grown"] += growth
            plot["watered_today"] = False

    state["day"] += 1

    if random.random() < 0.15:
        print("\n It rained overnight — all plots got a free watering!")
        for plot in state["plots"]:
            if plot is not None:
                plot["days_grown"] += 1

    print(f"\nA new day dawns. Welcome to day {state['day']}.")

MENU = """
1. View garden
2. Plant a seed
3. Water plots
4. Harvest ready crops
5. Sell harvest
6. Buy seeds
7. Advance to next day
8. Save and exit
"""

def main():
    print("=" * 40)
    print("           TEXT GARDEN SIMULATOR")
    print("=" * 40)

    state = load_game()
    display_garden(state)

    while True:
        print(MENU)
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            display_garden(state)
        elif choice == "2":
            plant_seed(state)
        elif choice == "3":
            water_plots(state)
        elif choice == "4":
            harvest_crops(state)
        elif choice == "5":
            sell_harvest(state)
        elif choice == "6":
            buy_seeds(state)
        elif choice == "7":
            advance_day(state)
        elif choice == "8":
            save_game(state)
            print("Garden saved. See you next time!")
            break
        else:
            print("Please enter a number from 1 to 8.")

if __name__ == "__main__":
    main()