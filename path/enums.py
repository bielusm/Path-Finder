'''A module of enums that need to be used globally'''

from enum import IntEnum

class Algorithms(IntEnum):
    '''Algorithms of the program'''
    BFS = 0
    DFS = 1

class FSM(IntEnum):
    '''The different states the program can be in'''
    RUN = 0
    RUNNING = 1
    RESET = 2
    SAVE = 3
    LOAD = 4
    WAIT = 5

class Locations(IntEnum):
    '''Each state a cell can be in'''
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3
    DISCOVERED = 4
    PATH = 5
    ACTIVE = 6
