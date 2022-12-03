import os
import updater
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.max_health = 50
        self.alive = True
        self.inventory_size = 50 #max size
        self.inventory_space = 50 #current available space in inventory
        self.gold = 0
        self.attack = 10
        self.defence = 0
        self.weapon = None
        self.armor = None
        updater.register(self)
    def __repr__(self):
        return_string = ""
        return return_string
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False
    def pickup(self, item):
        if self.inventory_space < item.weight:
            print("Too heavy to pick up! Drop something first")
        else:
            self.items.append(item)
            item.loc = self
            self.location.remove_item(item)
            self.inventory_space -= item.weight
    def drop(self, item_name): #drops 1 item with the given name, returns true if it removes an item, false otherwise
        for i in self.items:
            if i.name == item_name:
                self.inventory_space += i.weight
                self.items.remove(i)
                
                return True
        return False
    def dropall(self, item_name): #drops all items with the given name, returns nothing
        inventory_clear = True
        while inventory_clear:
            inventory_clear = self.drop(item_name)
                
    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")
    def attack_monster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print()
        run = False
        while self.health > 0 and mon.health > 0 and run == False:#combat loop, options are use item, attack, run
            print("Your health is " + str(self.health) + ".")
            print(mon.name + "'s health is " + str(mon.health) + ".")
            command = input("What do you do? ")
            command_words = command.split()
            match command_words[0].lower():
                
                case "attack":
                    mon.health -= self.attack
                    print("You hit the monster")
                case "run":
                    run = True
                case "use":
                    item = command[4:]
                    self.use_item(item)
                case other:
                    print("Not a valid command\nValid commands are:\nattack\nrun\nuse [item]")
            self.health -= (mon.attack - self.defence)
            print(f"{mon.name} struck you for {mon.attack} damage.")
            if run == True: 
                print("You ran away")
            
        if self.health > mon.health and run == False:
            self.health -= mon.health
            gold_gained = random.randint(1,20)
            self.gold += gold_gained
            print("You win. Your health is now " + str(self.health) + ".\n You gained " + str(gold_gained) + " gold.")
            mon.die()            
        elif run == False:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")
    def update(self):
        if self.health + 2 < self.max_health:#adds regeneration to player every time everything updates
            self.health += 3
    def use_item(self, item_name): #takes in name of item to use
        item_found = False
        for i in self.items:
            if i.name == item_name:
                item_type = i.use()
                item_found = True
                break
        if not item_found:
            print("Could not find item")
            return
        if item_type is None: #non-usable item
            ''
        elif item_type == "healing": #removes healing item after use
            self.health += i.healing
            self.drop(item_name)
        elif item_type == "weapon": #swaps weapon
            self.attack -= self.weapon.attack
            self.weapon = i
            self.attack += self.weapon.attack
        elif item_type == "armor": #swaps armor
            self.armor = i
            self.defence = i.defence
        else:
            print("could not use item")


