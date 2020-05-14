'''Current State of the program'''
from enum import Enum
from path.grid import Locations

class FSM(Enum):
    '''The different states the program can be in'''
    RUN = 0
    RESET = 1
    SAVE = 2
    LOAD = 3
    WAIT = 4

class State():
    '''Current state and context of program'''
    curr = FSM.WAIT
    context = dict(
                alg=0,
                current_tile=Locations.WALL)
