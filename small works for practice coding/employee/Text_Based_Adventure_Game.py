import random
import json
import os

SAVE_FILE = "adventure_save.json"


def create_player():
    print("\n=== CHARACTER CREATION ===")

    name = input("Enter your name: ")

    player = {
        "name": name,
        "health": 100,
        "energy": 100,
        "coins": 50,
        "weapon": "Wooden Sword",
        "damage": 10,
        "inventory": ["Small Potion"]
    }

    return player


def show_status(player):
    print("\n==========================")
    print(f"Name: {player['name']}")
    print(f"Health: {player['health']}")
    print(f"Energy: {player['energy']}")
    print(f"Coins: {player['coins']}")
    print(f"Weapon: {player['weapon']}")
    print(f"Damage: {player['damage']}")
    print(f"Inventory: {player['inventory']}")
    print("==========================")


def save_game(player):
    with open(SAVE_FILE, "w") as file:
        json.dump(player, file, indent=4)

    print("Game saved!")


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No saved game found.")
        return None

    with open(SAVE_FILE, "r") as file:
        player = json.load(file)

    print("Game loaded!")
    return player


def use_potion(player):
    if "Small Potion" not in player["inventory"]:
        print("You don't have a potion.")
        return

    if player["health"] == 100:
        print("Your health is already full.")
        return

    player["health"] += 30

    if player["health"] > 100:
        player["health"] = 100

    player["inventory"].remove("Small Potion")

    print("You used a potion.")
    print(f"Health: {player['health']}")


def combat(player, enemy_name, enemy_health, enemy_damage):
    print(f"\n⚔️ A {enemy_name} appeared!")

    while enemy_health > 0 and player["health"] > 0:

        print("\n----------------------")
        print(f"Your Health: {player['health']}")
        print(f"{enemy_name} Health: {enemy_health}")
        print("----------------------")

        print("1. Attack")
        print("2. Use Potion")
        print("3. Run")

        choice = input("Choose: ")

        if choice == "1":

            damage = random.randint(
                player["damage"] - 3,
                player["damage"] + 5
            )

            enemy_health -= damage

            print(f"You dealt {damage} damage.")

            if enemy_health <= 0:
                print(f"You defeated the {enemy_name}!")

                reward = random.randint(20, 60)
                player["coins"] += reward

                print(f"You received {reward} coins.")
                return True

            damage = random.randint(
                enemy_damage - 3,
                enemy_damage + 3
            )

            player["health"] -= damage

            print(
                f"The {enemy_name} dealt "
                f"{damage} damage to you."
            )

        elif choice == "2":
            use_potion(player)

        elif choice == "3":
            chance = random.randint(1, 100)

            if chance <= 50:
                print("You escaped!")
                return False
            else:
                print("You failed to escape!")

                damage = random.randint(
                    enemy_damage - 3,
                    enemy_damage + 3
                )

                player["health"] -= damage

        else:
            print("Invalid choice.")

    if player["health"] <= 0:
        print("\n💀 You died.")
        return False

    return True


def forest(player):
    print("\n🌲 You entered the dark forest.")

    player["energy"] -= 10

    event = random.randint(1, 4)

    if event == 1:
        print("You found a Small Potion!")
        player["inventory"].append("Small Potion")

    elif event == 2:
        coins = random.randint(10, 30)
        player["coins"] += coins

        print(f"You found {coins} coins!")

    elif event == 3:
        combat(
            player,
            "Wild Wolf",
            40,
            12
        )

    else:
        print("The forest is strangely quiet...")

    return player["health"] > 0


def cave(player):
    print("\n🪨 You entered a dangerous cave.")

    player["energy"] -= 20

    event = random.randint(1, 3)

    if event == 1:
        combat(
            player,
            "Goblin",
            60,
            15
        )

    elif event == 2:
        coins = random.randint(30, 80)
        player["coins"] += coins

        print(f"You discovered a treasure chest!")
        print(f"You received {coins} coins.")

    else:
        print("You found an empty room.")

    return player["health"] > 0


def shop(player):
    print("\n🏪 === SHOP ===")

    while True:

        print("\nYour coins:", player["coins"])

        print("1. Iron Sword - 100 coins")
        print("2. Golden Sword - 250 coins")
        print("3. Small Potion - 30 coins")
        print("4. Leave")

        choice = input("Choose: ")

        if choice == "1":

            if player["coins"] >= 100:
                player["coins"] -= 100
                player["weapon"] = "Iron Sword"
                player["damage"] = 20

                print("You bought an Iron Sword!")

            else:
                print("Not enough coins.")

        elif choice == "2":

            if player["coins"] >= 250:
                player["coins"] -= 250
                player["weapon"] = "Golden Sword"
                player["damage"] = 35

                print("You bought a Golden Sword!")

            else:
                print("Not enough coins.")

        elif choice == "3":

            if player["coins"] >= 30:
                player["coins"] -= 30
                player["inventory"].append("Small Potion")

                print("Potion added to inventory.")

            else:
                print("Not enough coins.")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def castle(player):
    print("\n🏰 You reached the ancient castle.")

    if player["weapon"] == "Golden Sword":

        print("\nThe castle guardian appears!")
        print("Only a legendary weapon can defeat him.")

        victory = combat(
            player,
            "Castle Guardian",
            120,
            25
        )

        if victory:
            print("\n👑 You defeated the guardian!")
            print("You discovered the legendary treasure.")
            print("🏆 YOU WON THE GAME!")
            return True

    else:

        print("\nThe castle guardian appears.")
        print("Your weapon is too weak.")

        choice = input(
            "Do you want to fight anyway? (y/n): "
        ).lower()

        if choice == "y":

            victory = combat(
                player,
                "Castle Guardian",
                120,
                25
            )

            if victory:
                print("\n🏆 Against all odds, you won!")
                return True

        else:
            print("You escaped the castle.")

    return False


def game(player):

    while player["health"] > 0:

        if player["energy"] <= 0:
            print("\nYou are too exhausted.")
            print("You need to rest.")

            player["energy"] = 100
            player["health"] += 20

            if player["health"] > 100:
                player["health"] = 100

            print("You rested.")
            continue

        print("\n==========================")
        print("       ADVENTURE")
        print("==========================")
        print("1. Explore Forest")
        print("2. Explore Cave")
        print("3. Visit Shop")
        print("4. Castle")
        print("5. Status")
        print("6. Save Game")
        print("7. Exit")
        print("==========================")

        choice = input("Choose: ")

        if choice == "1":
            if not forest(player):
                break

        elif choice == "2":
            if not cave(player):
                break

        elif choice == "3":
            shop(player)

        elif choice == "4":
            if castle(player):
                break

        elif choice == "5":
            show_status(player)

        elif choice == "6":
            save_game(player)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


def main():

    print("==========================")
    print("   DARK FOREST ADVENTURE")
    print("==========================")

    print("\n1. New Game")
    print("2. Load Game")

    choice = input("Choose: ")

    if choice == "1":
        player = create_player()
        game(player)

    elif choice == "2":
        player = load_game()

        if player:
            game(player)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()