# you can add items
# delete items
# edit items, or update them
# finished tasks go to the bottom of the list

def add_item(item):
    with open("to_do_list.txt", "a") as file:
        file.write(item + "\n")
    print(f"Added '{item}' to your to-do list.")

item = input("Would you like to add an item? (y/n) ")

if item.lower() == "y":
    item = input("What would you like to add to your to-do list? ")
    add_item(item)
else:
    print("No item added.")
    exit()

edit = input("Would you like to edit an item? (y/n) ")

if edit.lower() == "y":
    with open("to_do_list.txt", "r") as file:
        items = file.readlines()

    for index, item in enumerate(items):
        print(f"{index + 1}. {item.strip()}")

    item_number = int(input("Enter the number of the item you want to edit: "))
    if item_number < 1 or item_number > len(items):
        print("Invalid item number.")
        exit()
    else:
        new_item = input("Enter the new item: ")

    items[item_number - 1] = new_item + "\n"

    with open("to_do_list.txt", "w") as file:
        file.writelines(items)

    print(f"Updated item {item_number} to '{new_item}'.")

delete = input("Would you like to delete an item? (y/n) ")

if delete.lower() == "y":
    with open("to_do_list.txt", "r") as file:
        items = file.readlines()

    for index, item in enumerate(items):
        print(f"{index + 1}. {item.strip()}")

    item_number = int(input("Enter the number of the item you want to delete: "))
    if item_number < 1 or item_number > len(items):
        print("Invalid item number.")
        exit()
    else:
        deleted_item = items.pop(item_number - 1)

    with open("to_do_list.txt", "w") as file:
        file.writelines(items)

    print(f"Deleted '{deleted_item.strip()}' from your to-do list.")

finish = input("Would you like to mark an item as finished? (y/n) ") 

if finish.lower() == "y":
    with open("to_do_list.txt", "r") as file:
        items = file.readlines()

    for index, item in enumerate(items):
        print(f"{index + 1}. {item.strip()}")

    item_number = int(input("Enter the number of the item you want to mark as finished: "))
    if item_number < 1 or item_number > len(items):
        print("Invalid item number.")
        exit()
    else:
        items[item_number - 1] = items[item_number - 1].strip() + " ✓\n"

    with open("to_do_list.txt", "w") as file:
        file.writelines(items)

    print(f"Marked item {item_number} as finished.")
