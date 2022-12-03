import random

class Room:
    def __init__(self, description = None):
        self.desc = description
        if self.desc is None:
            self.desc = self.random_desc(random.randint(1,10))
        self.monsters = []
        self.exits = []
        self.items = []
    def add_exit(self, exit_name, destination):
        self.exits.append([exit_name, destination])
    def get_destination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                return e[1]
        return self
    def connect_rooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.add_exit(dir1, room2)
        room2.add_exit(dir2, room1)
    def exit_names(self):
        return [x[0] for x in self.exits]
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def add_monster(self, monster):
        self.monsters.append(monster)
    def remove_monster(self, monster):
        self.monsters.remove(monster)
    def has_items(self):
        return self.items != []
    def get_item_by_name(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def has_monsters(self):
        return self.monsters != []
    def get_monster_by_name(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False
    def random_neighbor(self):
        return random.choice(self.exits)[1]
    def random_desc(self, n):
        match n:
            case 1: return "A small stream runs through the center of this room."
            case 2: return "Every surface of the room is extremely polished, as if polished."
            case 3: return "Sketches of a floating monster with a massive eye cover the walls."
            case 4: return "The silhouette of a door has been drawn in yellow chalk on one wall. This room is unnaturally cold, a thin frost covers the walls and floor."
            case 5: return "Thick cobwebs cover the corner of the room"
            case 6: return "All surfaces in the room are covered in small holes of varying sizes."
            case 7: return "An empty treasure chest lies on the floor, broken open years ago."
            case 8: return "A light fog is present in the room, and no ceiling can be seen."
            case 9: return "Magical runes cover the door you came through, but the room seems normal."
            case 10: return "The ground feels unstable, and shudders as you walk on it"
    def random_direction(self):
        direction = random.randint(1,4)
        match direction:
            case 1: direction = ["north", "south"]
            case 2: direction = ["east", "west"]
            case 3: direction = ["south", "north"]
            case 4: direction = ["west", "east"]
        return direction