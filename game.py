import json
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

You wake in the quiet remains of an old metro system.  
Cold metal, empty tracks, water dripping from pipes you cannot see.  
A few rooms still connect through the dark.  
Move with commands like:

    go east
    go west
    get lantern
    get itemname

Your path unfolds one step at a time.  
Use your light, watch your choices, and keep moving.
""")




inventory = []

currentRoom = "entrance_shaft"

with open("rooms.json", "r") as f:
    rooms = json.load(f)
instructions()
while True:
    print(f"You are in the {currentRoom}!")
    move = input("> ")
    move = move.split(" ", 1)

    if move[0] =="go":
        if move[1] in rooms[currentRoom]["exits"]:
            currentRoom = rooms[currentRoom]["exits"][move[1]]
        print(f"You are now in the {currentRoom}!")

    print(move[0])
    if len(move) > 1:
        print(move[1])

    if move[0] == "get":
        item = rooms[currentRoom]["item"]

        if len(move) > 1 and move[1] == item:
            print(f'You got a {move[1]}!')
            inventory.append(move[1])
            rooms[currentRoom]["item"] = None
            print(inventory)
        else: print(f"You don't see a {move[1]} here!")