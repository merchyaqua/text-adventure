import time
from helpers import *

class Player:
    def __init__(self, name) -> None:
        self.__name = name
        self.__level = 1
        self.__backpack = Backpack()
        self.__handheld = None
        self.__damage = 1
    def hold(self, item):
        self.__handheld = item
        self.__damage = item.get_damage()
        print('Current handheld:', self.__handheld, 'damage', self.__damage)

    def get_handheld(self):
        return self.__handheld
    def get_name(self):
        return self.__name
    def get_level(self):
        return self.__level
    def get_damage(self):
        return self.__damage
    def get_backpack(self):
        return self.__backpack
    def take_item(self, item):
        self.__backpack.add_content(item)
    def drop_item(self, item):
        self.__backpack.remove_content(item)
        if self.get_handheld() == item:
            self.__handheld = None
    
    
    def __str__(self) -> str:
        return f"Name: {self.__name} \nLevel: {self.__level}\nHandheld: {self.__handheld}"


class Backpack:
    def __init__(self) -> None:
        self.__capacity = 10
        self.__free_space = self.__capacity
        self.__contents = []

    def upgrade(self, cap):
        self.__capacity += cap 
    def add_content(self, item):
        if item.get_size() <= self.__free_space:
            self.__contents.append(item)
            print(item, 'added to backpack')
            self.__free_space -= item.get_size()
            print('Free space remaining:', self.__free_space)
        else:
            print('Not enough space')
    def remove_content(self, item):
        self.__contents.remove(item)
        print(item, 'removed from backpack')
        self.__free_space += item.get_size()
    def get_contents(self):
        return self.__contents
    def __str__(self) -> str:
        return (
            'Capacity:'+ str(self.__capacity)+
            '\nFree space:'+str(self.__free_space)+
            '\nContents:' + str(list(str(item) for item in self.__contents))

        )
        

class Thing:
    def __init__(self, desc) -> None:
        self._description = desc
    def __str__(self) -> str:
        return self._description

class Room(Thing): 
    def __init__(self, desc) -> None:
        super().__init__(desc)
        self.__objects = []
        self.__items = []
        self.__beings = []
        self._exits = []

    def search(self):
        print("Here are items in the room:")
        if not menuify(self.__items):
            print('Nothing')
        return self.__items
            
    def enter(self):
        
        print('---'+str(self)+'---'+'\n\n') # room name
        time.sleep(1)
        print("You've encountered ", end='')
        if not menuify(self.__beings):
            print('nobody.')
        print('Objects in the room:')
        if not menuify(self.__objects):
            print(None)

        print('Exits:')
        exits = self.get_exits()
        menuify(exits)
    


    def add_item(self, thing):
        self.__items.append(thing)
    def remove_item(self, item):
        self.__items.remove(item)
    def add_object(self, thing):
        self.__objects.append(thing)
    def add_being(self, b):
        self.__beings.append(b)
    def add_exit(self, dest):
        self._exits.append(dest)
    
    
    def get_beings(self):
        return self.__beings
    def get_objects(self):
        return self.__objects
    def get_exits(self):
        return self._exits
        

class Being(Thing):
    def __init__(self, desc, health, damage) -> None:
        super().__init__(desc)
        self._health = health
        self._damage = damage

    def attacked(self, ouch):
        self._health -= ouch
        print(f"{str(self).split('-')[0]} health:{self._health}")
        if self._health <= 0:
            print(self._description, 'is dead. MURDERRRR')
            self._description = 'Dead ' + self._description
            self._damage = 0
        return self.attacks()
    def attacks(self):
        return self._damage
    

    
    def __str__(self) -> str:
        return(self._description) 


class Animal(Being):
    def __init__(self, desc, health, damage, noise) -> None:
        super().__init__(desc, health, damage)
        self.__noise = noise
    def attacked(self, ouch):
        super().attacked(ouch)
        print(self.__noise)




class Object(Thing):
    def __init__(self,desc) -> None:
        super().__init__(desc)
    def jump(self):
        print("You have jumped over it.")



class Item(Thing):
    def __init__(self, desc, size) -> None:
        super().__init__(desc)
        self.__size = size
        self._damage = 0
    def get_size(self):
        return self.__size
    def get_damage(self):
        return self._damage
    def __str__(self) -> str:
        return super().__str__() + ' - size '+str(self.__size)

class Weapon(Item):
    def __init__(self, desc, size, damage) -> None:
        super().__init__(desc, size)
        self._damage = damage
    def sharpen(self):
        self._damage += 1


class Game:
    def __init__(self) -> None:
        self.__player = None
        self.__rooms = []
        self.__current_room = None

    def set_player(self, p):
        self.__player = p
        
    def get_player(self) -> Player:
        return self.__player
    
    def get_current_room(self) -> Room:
        return self.__current_room
    def get_rooms(self) -> list:
        return self.__rooms
    def update_current_room(self, new):
        self.__current_room = new
    def add_room(self, room):
        self.__rooms.append(room)