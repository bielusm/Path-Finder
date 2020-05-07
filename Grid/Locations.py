'''Module containing different states a cell can be in'''
from enum import Enum

class Locations(Enum):
    '''Each state a cell can be in'''
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3
    DISCOVERED = 4
