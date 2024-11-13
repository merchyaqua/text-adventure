
from classes import *
from helpers import *
import time

commands = {'exit': 'Go to a room',
            'backpack': "Display backpack contents",
            'hold': "Hold an item in hand which is in the backpack",
            'search': "Search the room, shows items present",
            'pick up': "Pick up an item in the room and add it to backpack",
            'drop': "Remove an item from the player",
            'interact': "Interact with an object or being in the room",
            'quit': 'Quit the game',
            'profile': "Show profile of player"
            }
def print_commands():
    print('Valid commands:')
    for k, v in commands.items():
        print(k+': '+v)


def initialise_game():
    g = Game()
    name = input("What's your name? ")
    g.set_player(Player(name))
    atrium = Room('Atrium - welcome')
    atrium.add_being(Being('Butler', 10, 5))
    atrium.add_item(Weapon('Hockey stick', 9, 4))
    atrium.add_item(Item('Shoe', 1))

    bathroom = Room('Bathroom - fun place')
    bathroom.add_being(Being('Moaning Myrtle', 10, 2))
    bathroom.add_being(Animal('slug', 1, 1, 'slurp'))
    bathroom.add_object(Object('Toilet'))
    bathroom.add_item(Item('Tissue paper', 1))

    atrium.add_exit(bathroom)
    bathroom.add_exit(atrium)
    # put the rooms into the game
    g.add_room(atrium)
    g.add_room(bathroom)
    

    g.update_current_room(atrium)
    return g

def drown():
    for i in range(5):
        print('Glub'[:4-i]+ '..'*i)
        time.sleep(0.5)
    print('You have drowned.')
    


def interact(things, player) -> bool:
    ''' May lead to end of game. If returns true, it's end of game.'''
    print("You've chosen to interact.")
    if menuify(things):
        thing = menu_input(things,'Interact with: ')
        if type(thing) == Being or type(thing) == Animal:
            option = input('Attack it? y/n: ')
            if option == 'y':
                thing.attacked(player.get_damage())
        elif type(thing) == Object:
            option = input('Jump over it? y/n: ')
            if option == 'y':
                thing.jump()
                if str(thing) == 'Toilet':
                    drown()
                    return True

    else:
        print('Nothing to interact with.')
    
    return False


def main():
    game = initialise_game()
    print_commands()
    end = False
    
    while not end:
        current = game.get_current_room()
        current.enter()

        while not end:
            if not current.get_exits(): # no exits for this room
                end = True
                break
            p = game.get_player()
            print()
            action = input('What would you like to do? ')
            
            match action:
                case 'exit':
                    menuify(current.get_exits())
                    if dest := menu_input(current.get_exits(), 'Exit to: '):
                        game.update_current_room(dest)
                        break # new room
                case 'backpack':
                    print(p.get_backpack())
                case 'hold':
                    if b := p.get_backpack().get_contents():
                        menuify(b)
                        item = menu_input(b, 'Which item to hold:')
                        if item:
                            p.hold(item)
                    else:
                        print('Nothing in backpack to hold')

                case 'search':
                    current.search()
                
                case 'pick up':                    
                    if stuff := current.search():
                        option = menu_input(stuff, 'Pick up: ')
                        if option:
                            p.take_item(option)
                        current.remove_item(option)
                    else:
                        print('Nothing to pick up')
                case 'drop':    
                    if stuff := p.get_backpack().get_contents():
                        menuify(stuff)
                        option = menu_input(stuff, 'Drop: ')
                        if option:
                            p.drop_item(option)
                        current.add_item(option)
                    else:
                        print('Nothing to drop')

                case 'interact':
                    # bypassing private: 
                    # being = menu_input(current._Room__beings, 'Interact with: ')
                    thing = input('Object or being?')

                    if thing == 'object':
                        end = interact(current.get_objects(), p) 
                    elif thing == 'being':
                        end = interact(current.get_beings(), p)
                    else:
                        print("You can't interact with that.")
                case 'profile':
                    print(p)
                case 'quit':
                    end = True

                case _:
                    print_commands()
    print('Thanks for playing. ')
    print("Your stats:")
    print(p)
       

main()