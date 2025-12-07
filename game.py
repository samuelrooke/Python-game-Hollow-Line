import json
import random

# ------------- LOADING DATA -------------

with open("rooms.json", "r") as f:
    rooms = json.load(f)

# ------------- GLOBAL STATE -------------

inventory = []
currentRoom = "entrance_shaft"

drifter_room = "rail_pit"       # starting location for the Drifter
flare_active = False
flare_timer = 0

fear = 0                        # 0 to 10
drifter_met_with_flare = False  # for an optional second encounter ending


# ------------- UI AND FLAVOR -------------

def instructions():
    print("""
 ██░ ██  ▒█████   ██▓     ██▓     ▒█████   █     █░    ██▓     ██▓ ███▄    █ ▓█████ 
▓██░ ██▒▒██▒  ██▒▓██▒    ▓██▒    ▒██▒  ██▒▓█░ █ ░█░   ▓██▒    ▓██▒ ██ ▀█   █ ▓█   ▀ 
▒██▀▀██░▒██░  ██▒▒██░    ▒██░    ▒██░  ██▒▒█░ █ ░█    ▒██░    ▒██▒▓██  ▀█ ██▒▒███   
░▓█ ░██ ▒██   ██░▒██░    ▒██░    ▒██   ██░░█░ █ ░█    ▒██░    ░██░▓██▒  ▐▌██▒▒▓█  ▄ 
░▓█▒░██▓░ ████▓▒░░██████▒░██████▒░ ████▓▒░░░██▒██▓    ░██████▒░██░▒██░   ▓██░░▒████▒
 ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒     ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
 ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░     ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░
 ░  ░░ ░░ ░ ░ ▒    ░ ░     ░ ░   ░ ░ ░ ▒    ░   ░       ░ ░    ▒ ░   ░   ░ ░    ░   
 ░  ░  ░    ░ ░      ░  ░    ░  ░    ░ ░      ░           ░  ░ ░           ░    ░  ░

Welcome to Hollow Line.

Commands you can use:
    go east / west / north / south
    get itemname -- TAKE ITEMS
    use flare -- USE ITEM
    search -- SEARCH FOR USEFUL ITEMS
    read -- DESCRIPTION OF ROOM
    look -- REPEAT ROOM
    inventory
    quit

Move with care, check each room and gather what you need.
""")


def status():
    print("------------------")
    print(f"Current room: {currentRoom}")
    print(f"Inventory: {inventory}")
    print(f"Fear: {fear}/10")


def show_room():
    room = rooms[currentRoom]

    print()
    print(room["name"])
    print(room["description"])

    item = room.get("item")
    if item:
        print(f"You see a {item}.")

    exits = ", ".join(room["exits"].keys())
    print(f"Exits: {exits}")
    print()


ambient_lines = [
    "You hear a faint scrape far down the tunnel.",
    "Cold air moves past you as if the metro still breathes.",
    "A drop of water falls somewhere in the dark.",
    "Metal shifts under old tension.",
    "Your light flickers, then steadies.",
    "Something rattles in the distance and fades."
]


def ambient():
    if random.random() < 0.25:
        print(random.choice(ambient_lines))


# ------------- WORLD EVENTS -------------

def power_failure():
    global fear
    if random.random() < 0.10:
        print("The weak lights in your mind go out for a moment.")
        fear = min(fear + 1, 10)


def drifter_hint():
    room = rooms[currentRoom]
    exits = room["exits"].values()

    if drifter_room in exits:
        print("You sense movement in a nearby tunnel.")


def move_drifter():
    global drifter_room
    exits = list(rooms[drifter_room]["exits"].values())

    if not exits:
        return

    # when flare is active, the Drifter tries to avoid the player room
    if flare_active:
        filtered = [r for r in exits if r != currentRoom]
        if filtered:
            exits = filtered

    drifter_room = random.choice(exits)


def drifter_encounter():
    global drifter_met_with_flare
    if currentRoom != drifter_room:
        return False

    print("A tall outline blocks the tunnel ahead, still and wrong against the dark.")

    if "flare" in inventory and flare_active:
        if not drifter_met_with_flare:
            print("The burning flare drives the shape back. It folds into shadow and withdraws.")
            drifter_met_with_flare = True
            move_drifter()
            return False
        else:
            print("Again the flare burns bright. This time the shape does not retreat.")
            print("Light cuts through its form until nothing solid remains.")
            print("Dust drifts on the air. The metro falls quiet around you.")
            print("Whatever haunted these lines will not return.")
            return True
    else:
        print("You reach for safety that is not there in time.")
        print("A Cold presence closes in and the tunnels claim you.")
        print(" YOU DIED -- GAME OVER")
        return True


# ------------- MAIN GAME -------------

def main():
    global currentRoom, flare_active, flare_timer, fear

    instructions()
    show_room()
    status()

    while True:
        # world tick before input
        ambient()
        drifter_hint()
        power_failure()

        # fear grows if Drifter is nearby and no active flare
        if drifter_room in rooms[currentRoom]["exits"].values() and not flare_active:
            fear = min(fear + 1, 10)

        # flare burn down
        if flare_active:
            flare_timer -= 1
            if flare_timer <= 0:
                flare_active = False
                print("The flare dies out. Shadows thicken around you.")

        if fear >= 10:
            print("Your nerves give out. You run without direction until the maze takes you.")
            break

        move = input("> ").strip().lower().split(" ", 1)

        if not move[0]:
            continue

        action = move[0]
        arg = move[1] if len(move) > 1 else None

        room = rooms[currentRoom]

        if action == "go":
            if not arg:
                print("Go where.")
            elif arg in room["exits"]:
                if "one_way" in room and arg in room["one_way"]:
                    print("You can go this way, but you will not return by the same route.")
                currentRoom = room["exits"][arg]
                show_room()
                status()
            else:
                print("No path that way.")

        elif action == "get":
            if not arg:
                print("Take what.")
            else:
                room_item = room.get("item")
                if room_item is None:
                    print("Nothing to pick up here.")
                elif arg == room_item:
                    print(f"You pick up the {arg}.")
                    inventory.append(arg)
                    room["item"] = None
                else:
                    print(f"You do not see a {arg} here.")

        elif action == "use":
            if arg == "flare":
                if "flare" in inventory:
                    flare_active = True
                    flare_timer = 6
                    print("The flare bursts into harsh light and heat.")
                else:
                    print("You do not have a flare.")
            else:
                print("Use what.")

        elif action == "search":
            if "secret" in room:
                print(room["secret"])
                hidden = room.get("hidden_item")
                if hidden:
                    print(f"You find a {hidden}.")
                    inventory.append(hidden)
                    room["hidden_item"] = None
            else:
                print("You search the area but find nothing new.")

        elif action == "read":
            if "notes" in room:
                print(room["notes"])
            else:
                print("Nothing here to read.")

        elif action == "look":
            show_room()
            status()

        elif action in ("inventory", "inv", "i"):
            print(f"Inventory: {inventory}")

        elif action in ("quit", "exit"):
            print("You sit down among the dust and silence, letting the tunnels have this story.")
            break

        else:
            print("You mutter a sound the tunnels do not understand.")

        # Drifter moves and may meet you
        move_drifter()
        if drifter_encounter():
            break

        # check endings after each full turn

        # Ending 1: Rust Gate with blowtorch
        if currentRoom == "rust_gate" and "blowtorch" in inventory:
            print("You cut through the thick red metal of the Rust Gate.")
            print("A stair climbs upward into biting cold air.")
            print("You step out above the old lines under a pale sky.")
            break

        # Ending 2: Archive escape with card and chip
        if currentRoom == "signal_archive" and "old_card" in inventory and "chip" in inventory:
            print("You slot the chip into a cracked console and swipe the old card.")
            print("Somewhere below, locks release with a deep mechanical sigh.")
            print("A hidden service passage opens that climbs for a long time.")
            print("Many steps later you reach an empty control tower that still looks out on the city.")
            print("You leave the metro behind.")
            print("YOU WON")
            break


if __name__ == "__main__":
    main()
