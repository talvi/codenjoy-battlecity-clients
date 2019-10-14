from math import sqrt

from battlecityclient.internals.element import Element
from battlecityclient.internals.point import Point


class Board:
    """ Class describes the Board field for Bomberman game."""
    def __init__(self, board_string):
        self._string = board_string.replace('\n', '')
        self._len = len(self._string)  # the length of the string
        self._size = int(sqrt(self._len))  # size of the board 
        #print("Board size is sqrt", self._len, self._size)

    def _find_all(self, element):
        """ Returns the list of points for the given element type."""
        _points = []
        _a_char = element.get_char()
        for i, c in enumerate(self._string):
            if c == _a_char:
                 _points.append(self._strpos2pt(i))
        return _points

    def get_at(self, x, y):
        """ Return an Element object at coordinates x,y."""
        return Element(self._string[self._xy2strpos(x, y)])

    def has_element_at(self, x, y, element_object):
        """ Return True if Element is at x,y coordinates."""
        return element_object == self.get_at(x, y)

    def is_barrier_at(self, x, y):
        """ Return true if barrier is at x,y."""
        return Point(x, y) in self.get_barriers()

    def get_my_position(self):
        """ Return the point where your tank is."""
        points = set()
        points.update(self._find_all(Element('TANK_UP')))
        points.update(self._find_all(Element('TANK_DOWN')))
        points.update(self._find_all(Element('TANK_LEFT')))
        points.update(self._find_all(Element('TANK_RIGHT')))
        assert len(points) <= 1, "There should be only one tank"
        return list(points)[0]

    def get_ai_positions(self):
        """ Return the list of points for other ai tanks."""
        points = set()
        points.update(self._find_all(Element('AI_TANK_DOWN')))
        points.update(self._find_all(Element('AI_TANK_LEFT')))
        points.update(self._find_all(Element('AI_TANK_UP')))
        points.update(self._find_all(Element('AI_TANK_RIGHT')))
        return list(points)

    def get_other_tank_positions(self):
        """ Return the list of points for other tanks."""
        points = set()
        points.update(self._find_all(Element('OTHER_TANK_LEFT')))
        points.update(self._find_all(Element('OTHER_TANK_RIGHT')))
        points.update(self._find_all(Element('OTHER_TANK_UP')))
        points.update(self._find_all(Element('OTHER_TANK_DOWN')))
        return list(points)

    def get_bullets_positions(self):
        """ Return the list of points for bullets."""
        points = set()
        points.update(self._find_all(Element('BULLET')))
        return list(points)

    def get_constructions_positions(self):
        """ Returns the list of constructions Element Points."""
        points = set()
        points.update(self._find_all(Element('CONSTRUCTION')))
        return list(points)
 
    def get_destroyed_constructions_positions(self):
        """ Returns the list of destroyed constructions Element Points."""
        points = set()
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_DOWN')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_UP')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_LEFT')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_RIGHT')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_DOWN_TWICE')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_UP_TWICE')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_LEFT_TWICE')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_RIGHT_TWICE')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_LEFT_RIGHT')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_UP_DOWN')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_UP_LEFT')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_RIGHT_UP')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_DOWN_LEFT')))
        points.update(self._find_all(Element('CONSTRUCTION_DESTROYED_DOWN_RIGHT')))
        return list(points)

    def get_wall_positions(self):
        """Returns the set of undestroyable walls"""
        points = set()
        points.update(self._find_all(Element('BATTLE_WALL')))
        return list(points)

    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self.get_wall_positions())
        points.update(self.get_constructions_positions())
        points.update(self.get_destroyed_constructions_positions())
        points.update(self.get_ai_positions())
        points.update(self.get_other_tank_positions())
        return list(points)


    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self.get_wall_positions())
        return list(points)
        
    def is_near_to_element(self, x, y, elem):
        _is_near = False
        if not Point(x, y).is_bad(self._size):
            _is_near = (self.has_element_at(x + 1, y, elem) or
                        self.has_element_at(x - 1, y, elem) or
                        self.has_element_at(x, 1 + y, elem) or
                        self.has_element_at(x, 1 - y, elem))
        return _is_near

    def has_ai_at(self, x, y):
        return Point(x, y) in self.get_ai_positions()

    def has_other_hero_at(self, x, y):
        return Point(x, y) in self.get_other_tank_positions()

    def has_wall_at(self, x, y):
        return Point(x, y) in self.get_wall_positions()

    def get_count_elements_near_to_point(self, x, y, elem):
        """ Counts the number of occurencies of elem nearby """
        _near_count = 0
        if not Point(x, y).is_bad(self._size):
            for _x, _y in ((x + 1, y), (x - 1, y), (x, 1 + y), (x, 1 - y)):
                if self.has_element_at(_x, _y, elem):
                    _near_count += 1
        return _near_count

    def to_string(self):
        return ("Board:\n{brd}\Me at: {mbm}\nOther Tanks "
                "at: {obm}\nAI at: {mcp}\nBullets at:".format(
                                          brd=self._line_by_line(),
                                          mbm=self.get_my_position(),
                                          obm=self.get_other_tank_positions(),
                                          mcp=self.get_ai_positions(),
                                          dwl=self.get_bullet_positions())
        )

    def print_board(self):
        print(self._line_by_line())

    def _line_by_line(self):
        return '\n'.join([self._string[i:i + self._size]
                              for i in range(0, self._len, self._size)])

    def _strpos2pt(self, strpos):
        return Point(*self._strpos2xy(strpos))

    def _strpos2xy(self, strpos):
        return (strpos % self._size, strpos // self._size)

    def _xy2strpos(self, x, y):
        return self._size * y + x


if __name__ == '__main__':
    raise RuntimeError("This module is not designed to be ran from CLI")
