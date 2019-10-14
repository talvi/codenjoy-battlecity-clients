_ELEMENTS = dict(

    CONSTRUCTION = '╬',

    CONSTRUCTION_DESTROYED_DOWN = '╩',
    CONSTRUCTION_DESTROYED_UP = '╦',
    CONSTRUCTION_DESTROYED_LEFT = '╠',
    CONSTRUCTION_DESTROYED_RIGHT = '╣',
    CONSTRUCTION_DESTROYED_DOWN_TWICE = '╨',
    CONSTRUCTION_DESTROYED_UP_TWICE = '╥',
    CONSTRUCTION_DESTROYED_LEFT_TWICE = '╞',
    CONSTRUCTION_DESTROYED_RIGHT_TWICE = '╡',
    CONSTRUCTION_DESTROYED_LEFT_RIGHT = '│',
    CONSTRUCTION_DESTROYED_UP_DOWN = '─',
    CONSTRUCTION_DESTROYED_UP_LEFT = '┌',
    CONSTRUCTION_DESTROYED_UP_RIGHT = '┐',
    CONSTRUCTION_DESTROYED_DOWN_LEFT = '└',
    CONSTRUCTION_DESTROYED_DOWN_RIGHT = '┘',

    BULLET = '•',

    AI_TANK_UP = '?',
    AI_TANK_RIGHT = '»',
    AI_TANK_DOWN = '¿',
    AI_TANK_LEFT = '«',

    OTHER_TANK_UP = '˄',
    OTHER_TANK_RIGHT = '˃',
    OTHER_TANK_DOWN = '˅',
    OTHER_TANK_LEFT = '˂',

    TANK_UP = '▲',
    TANK_RIGHT = '►',
    TANK_DOWN = '▼',
    TANK_LEFT = '◄',

    BATTLE_WALL = '☼',
    BANG = 'Ѡ',

    NONE = ' '

)


def value_of(char):
    """ Test whether the char is valid Element and return it's name."""
    for value, c in _ELEMENTS.items():
        if char == c:
            return value
    else:
        raise AttributeError("No such Element: {}".format(char))


class Element:
    """ Class describes the Element objects for Bomberman game."""
    def __init__(self, n_or_c):
        """ Construct an Element object from given name or char."""
        for n, c in _ELEMENTS.items():
            if n_or_c == n or n_or_c == c:
                self._name = n
                self._char = c
                break
        else:
            raise AttributeError("No such Element: {}".format(n_or_c))
            
    def get_char(self):
        """ Return the Element's character."""
        return self._char
    
    def __eq__(self, otherElement):
        return (self._name == otherElement._name and
                self._char == otherElement._char)

if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")
