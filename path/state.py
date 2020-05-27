'''Current State of the program'''
from path.enums import FSM, Locations


class State():
    '''Current state and context of program'''

    def __init__(self, grid_size):
        self.curr = FSM.WAIT
        self.context = dict(
            alg=0,
            current_tile=Locations.WALL,
            map=0,
            grid_size=grid_size)
