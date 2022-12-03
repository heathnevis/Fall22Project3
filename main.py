from room import Room
from player import Player
from item import Item, HealingItem, Armor, Weapon
from monster import Monster
import os
import updater
import random

player = Player()

def create_world():# need to change world gen to have rooms (~8) generate with random connections
    a = Room("You are in room 1")
    b = Room("You are in room 2")
    c = Room("You are in room 3")
    d = Room("You are in room 4")
    room_list = [] #list of all rooms being randomly made
    for i in range(8):
        new_room = Room()
        room_list.append(new_room)
    for i in room_list: #pick a random room to connect to, repeating twice
        stall_count = 0 #here to prevent infinite looping by accident
        for j in range(2):
            connecting_room = room_list[random.randint(0,7)]
            while len(connecting_room.exits) >= 4 or connecting_room == i:
                connecting_room = room_list[random.randint(0,7)] #ensures that the room to connect to has an available exit
                stall_count += 1
                if stall_count > 200:
                    break
            direction1, direction2 = i.random_direction()
            while direction2 in connecting_room.exits or direction1 in i.exits:
                direction1, direction2 = i.random_direction()
                stall_count += 1
                if stall_count > 200:
                    break
            if stall_count > 200:
                break
            Room.connect_rooms(i, direction1, connecting_room, direction2)
        
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    Room.connect_rooms(a, "south",  room_list[0], "north")

    i = Item("Rock", "This is just a rock.", 2)
    j = HealingItem("healing potion", "heals 10 hp", 5, 10)
    i.put_in_room(a)
    j.put_in_room(a)
    player.location = a
    Monster("Bob the monster", 20, a)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_situation():
    clear()
    print(player.location.desc)
    print()
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.has_items():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(e)
    print()

def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    create_world()
    playing = True
    wait_time = 0
    while playing and player.alive:
        print_situation()
        command_success = False
        time_passes = False
        if wait_time > 0:
            time_passes = True
            command_success = True
            wait_time -= 1
        while not command_success:
            command_success = True
            command = input("What now? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "go":   #cannot handle multi-word directions
                    okay = player.go_direction(command_words[1]) 
                    if okay:
                        time_passes = True
                    else:
                        print("You can't go that way.")
                        command_success = False
                case "pickup":  #can handle multi-word objects
                    target_name = command[7:] # everything after "pickup "
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        player.pickup(target)
                    else:
                        print("No such item.")
                        command_success = False
                case "drop": 
                    target_name = command[5:] #everything after 'drop'
                    if player.drop(target_name):
                        print(f"You dropped {target_name}")
                    else:
                        print("No such item.")
                        command_success = False
                case "dropall":
                    target_name = command[9:]
                    player.dropall(target_name)
                case "inventory":
                    player.show_inventory()
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "attack":
                    target_name = command[7:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                        if random.random() > 0.5: #gives a chance for an item to drop (~50%)
                            item_type = random.randint(1,4)
                            if item_type == 1:
                                loot = Item()
                            if item_type == 2:
                                loot = HealingItem()
                            if item_type == 3:
                                loot = Weapon()
                                ''
                            if item_type == 4:
                                loot = Armor()
                                ''
                            player.location.items.append(loot)
                    else:
                        print("No such monster.")
                        command_success = False
                case "wait":
                    time = command[5:]
                    if time == '':
                        wait_time = 1
                    else:
                        wait_time = int(time)
                case "inspect":
                    target_found = False
                    target_name = command[8:]
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        target.describe()
                        target_found = True
                    else:
                        for i in player.items:
                            if i.name == target_name:
                                i.describe()
                                target_found = True
                                break
                    if not target_found:
                        print("Could not find item")
                        command_success = False    
                case "use":
                    target_name = command[4:]
                    player.use_item(target_name)
                    
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()




'''
Points tracker
Total: 23
    drop: 1
    inventory size: 2
    wait: 1
    regeneration: 2
    inspect: 2
    random world: 3
    bigger world: 2
    armor: 2
    weapons: 2
    loot: 3
    player attributes: 3 //could do more with this, but defence/attack counts

Needs work:
    dropall not working properly
    more monsters, new classes? (monster that steals an item?)
    randomize world generation, too many exits(multiple of the same direction showing up)
        add a check if the current room being considered already has 4 exits, then skip if it does
'''