import random
import updater
class Monster:
    def __init__(self, name, health, room):
        self.name = name
        self.attack = random.randint(1,10)
        if self.name == "default":
            self.name = self.random_name(random.randint(1,10))
        self.health = health
        if self.health == -1:
            self.health = random.randint(1,50)
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
    def random_name(self,n):
        match n:
            case 1: return "Ogre"
            case 2: return "Goblin"
            case 3: return "Kobald"
            case 4: return "Bob"
            case 5: return "Baby Dragon"
            case 6: return "Skeleton"
            case 7: return "Larry"
            case 8: return "Slime"
            case 9: return "Zombie"
            case 10: return "Fire Elemental"

class Boss(Monster):
    def __init__(self, room):
        super().__init__("Beholder",100, room)
        self.attack = 10
        self.phase = 1
    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
        if self.phase < 3:
            self.phase += 1
            self.attack += 5
            self.health = 150
            updater.register(self)
            self.room.add_monster(self)

    
    