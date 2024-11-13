def menuify(ls):
    ''' print a numbered menu for a list'''
    if not ls:
        return False
    for i in range(len(ls)):
        print(f'{i+1}. {ls[i]}')
    return True

def menu_input(ls, prompt):
    if not ls:
        return False
    try:
        option = int(input(prompt)) -1
        return ls[option]
    except IndexError:
        print('No such option.')
    except ValueError:
        print('Please only enter numbers on menu.')
    return False


