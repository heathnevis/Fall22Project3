import random
import updater
class Monster:
    def __init__(self, name = None, health = None, room = None):
        self.name = name
        self.attack = random.randint(1,10)
        if self.name is None:
            self.name = self.random_name(random.randint(1,10))
        self.health = health
        if self.health is None:
            self.health = random.randint(1,50)
            if self.name == "Beholder":
                self.health = 70
                self.attack = 15
        self.max_health = self.health
        self.room = room
        room.add_monster(self)
        updater.register(self)
    def update(self):
        if random.random() < .5:
            self.move_to(self.room.random_neighbor())
    def move_to(self, room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)
    def die(self):
        #generate a new loot item and add it to the room
        self.room.remove_monster(self)
        updater.deregister(self)
    def random_name(n):
        match n:
            case 1: return "Ogre"
            case 2: return "Goblin"
            case 3: return "Kobald"
            case 4: return "Bob"
            case 5: return "Baby Dragon"
            case 6: return "Skeleton"
            case 7: return "Beholder"
            case 8: return "Slime"
            case 9: return "Zombie"
            case 10: return "Fire Elemental"
