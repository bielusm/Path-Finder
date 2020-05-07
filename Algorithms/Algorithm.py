'''This module holds the basic Algorithm that Algorithms inheirt from and Holds the State Enum'''
import queue
from abc import ABC
from enum import Enum, auto
from grid.locations import Locations

class State(Enum):
    '''Every State an Algorithm can be in'''
    SOLVING = auto()
    TRACING = auto()
    SOLVED = auto()
    RESET = auto()

class Algorithm(ABC):
    '''A class containing functions and members that each algorithm needs'''
    def __init__(self, grid):
        self.grid = grid
        self._state = State.RESET
        self._parent_map = {}
        self._parent = None
        # Parent Map from https://stackoverflow.com/a/12864196

    def reset(self):
        '''Resets members to initial settings'''
        self._parent_map = {}
        self._parent = None

    def trace_path(self):
        '''Updates grid step by step so a path is drawn from the end to the start'''
        row, col = self._parent
        self.grid.update_box(row, col, Locations.END)

        if self._parent == self.grid.start:
            self._state = State.RESET
            return False

        self._parent = self._parent_map[self._parent]
        return True

    def get_edges(self, row, col):
        '''Gets all edges of a cell (ignoring walls) and adds the to a queue'''
        def check_and_add(i, j):
            if not self.grid.get_val(i, j) == Locations.WALL:
                edges.put((i, j))

        edges = queue.Queue()
        if not row == 0:
            check_and_add(row - 1, col)
        if not row == self.grid.width - 1:
            check_and_add(row + 1, col)
        if not col == 0:
            check_and_add(row, col - 1)
        if not col == self.grid.height - 1:
            check_and_add(row, col + 1)
        return edges

    def step(self):
        '''One step of the algorithm, to be overriden by different algorithms'''
