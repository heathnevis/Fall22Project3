from room import Room
from player import Player
from item import Item, HealingItem, Armor, Weapon
from monster import Monster, Boss
import os
import updater
import random

player = Player()

def create_world():
    a = Room("You are in room 1")
    b = Room("You are in room 2")
    c = Room("You are in room 3")
    d = Room("You are in room 4")
    room_list = [] #list of all rooms being randomly made
    for i in range(3):
        new_room = Room()
        room_list.append(new_room)
    for i in room_list: #pick a random room to connect to, repeating twice
        for j in range(3): #makes sure there's at least two exits to each room
            if len(i.exits) > 3: #checks if there are already enough exits
                break
            for connecting_room in room_list:
                if len(connecting_room.exits) < 4 and connecting_room != i:#ensures that the room to connect to has an available exit
                    break
            direction1, direction2 = i.random_direction()
            while direction2 in connecting_room.exits or direction1 in i.exits:
                direction1, direction2 = i.random_direction()
            Room.connect_rooms(i, direction1, connecting_room, direction2)
        if random.random() < 0.7:
            mon = Monster("default", -1, i)        
        
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    Room.connect_rooms(a, "south",  room_list[0], "north")

    i = Item("Rock", "This is just a rock.", 2)
    j = HealingItem("healing potion", "heals 20 hp", 5, 20)
    i.put_in_room(a)
    j.put_in_room(a)
    player.location = a
    Monster("Bob the monster", 20, a)
    return room_list


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
    print("drop <item> -- drops the item")
    print("dropall <item> -- drops all items of the same name")
    print("attack <monster name> -- starts combat with monster")
    print("wait -- just kind of sit there")
    print("inspect <item> -- prints description and stats of item")
    print("quit -- quits the game")
    print("use <item> -- uses or equips the item")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    rooms = create_world()
    playing = True
    wait_time = 0
    total_time = 0 #counter for spawning the boss
    boss_alive = True
    boss = None
    command = input("You have been trapped in a dungeon. It seems that the only way out is to defeat the rule of this dungeon, the Beholder.\nPress enter to continue...")
    while playing and player.alive and boss_alive:
        total_time += 1
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
                        print("You picked up the", target_name)
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
                    target_name = command[8:]
                    player.dropall(target_name)
                case "inventory":
                    player.show_inventory()
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "quit":
                    playing = False
                case "attack":
                    target_name = command[7:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                        if target.name == "Beholder": #boss defeat behavior
                            loot = HealingItem("Elixer of life", "The Beholder accidentally dropped this. It feels powerful", 10, 99)
                            player.location.items.append(loot)
                            #boss.room = rooms[random.randint(0,length-1)]
                        elif random.random() > 0.3: #gives a chance for an item to drop (~70%)
                            item_type = random.randint(1,4)
                            if item_type == 1:
                                loot = Item()
                            if item_type == 2:
                                loot = HealingItem()
                            if item_type == 3:
                                loot = Weapon()
                            if item_type == 4:
                                loot = Armor()
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
                    show_message = input("Press enter to continue...")
                    
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()
        if total_time > 20:#spawns boss after a bit
            length = len(rooms)
            boss_room = rooms[random.randint(0,length-1)]
            if boss is None:
                boss = Boss(boss_room)
            if boss.phase > 2: #ends the game if the boss is killed
                boss_alive = False
            boss.move_to(rooms[random.randint(0,length-1)])
    if not boss_alive:
        print("You defeated the Beholder, freeing youself. Congratulations!")




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
    more monsters, new classes? (monster that steals an item?)
    work on boss behavior, make it end the game if the second phase is beat
    single use damage items?
'''