import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name = None, desc = None, weight = None):
        self.name = name
        self.desc = desc
        self.loc = None
        self.weight = weight
        if self.name == None and self.desc == None and self.weight == None:#generating a random item
            self.weight = random.randint(1,7)
            self.name = self.random_name(random.randint(1,10)) #makes a random description
            self.desc = self.random_desc(random.randint(1,10)) #makes a random description
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def put_in_room(self, room):
        self.loc = room
        room.add_item(self)
    def use(self):
        print("Nothing happened")
        return None
    def random_name(self, num):
        match num:
            case 1:
                return("Glow Stick")
            case 2:
                return("desc")
            case 3:
                return("desc")
            case 4:
                return("desc")
            case 5:
                return("desc")
            case 6:
                return("desc")
            case 7:
                return("desc")
            case 8:
                return("desc")
            case 9:
                return("desc")
            case 10:
                return("desc")
    def random_desc(self, num):
        match num:
            case 1:
                return(f"It's just a {self.name}")
            case 2:
                return(f"This {self.name} glows with power")
            case 3:
                self.weight += 1
                return("It's oddly heavy")
            case 4:
                self.weight -= 1
                return("It feels hollow")
            case 5:
                return("desc")
            case 6:
                return("desc")
            case 7:
                return("desc")
            case 8:
                return("desc")
            case 9:
                return("desc")
            case 10:
                return("desc")


#Eventually going to add weapons and armor, which inherit from item
#idea: usable items inherits from item, with weapons and armor as children, includes stat affecting items
class HealingItem(Item):
    def __init__(self, name = None, desc = None, weight = None, healing_value = None):
        super().__init__(name, desc, weight)
        
        if healing_value == None:
            healing_value = random.randint(1,50)
        self.healing = healing_value
    def use(self):
        print(f"you healed yourself for {self.healing}")
        return "healing"

class Armor(Item): #need to add unique desc/name
    def __init__(self, name = None, desc = None, weight = None, defence_value = None):
        super().__init__(name, desc, weight)
        if defence_value == None:
            defence_value = random.randint(0,20)
        self.defence = defence_value
        self.desc += f"\nGives {self.defence} defence"
    def use(self):
        print("You put on the armor")

class Weapon(Item):#need to add unique desc/name
    def __init__(self, name = None, desc = None, weight = None, attack_value = None):
        super().__init__(name, desc, weight)
        if attack_value == None:
            attack_value = random.randint(0,20)
        self.attack = attack_value
        self.desc += f"\nGives {self.attack} attack"
    def use(self):
        print("You switch your weapon")