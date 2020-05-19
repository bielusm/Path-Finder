'''Current State of the program'''
from path.enums import FSM, Locations


class State():
    '''Current state and context of program'''
    curr = FSM.WAIT
    context = dict(
                alg=0,
                current_tile=Locations.WALL,
                map=0)
