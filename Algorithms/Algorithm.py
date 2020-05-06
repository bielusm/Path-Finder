from abc import ABC
from enum import Enum, auto
from Grid.Locations import Locations
import queue


class State(Enum):
    SOLVING = auto()
    TRACING = auto()
    SOLVED = auto()
    RESET = auto()


class Algorithm(ABC):
    def __init__(self, grid):
        self.grid = grid
        self._state = State.RESET
        self._parent_map = {}
        self._parent = None
        # Parent Map from https://stackoverflow.com/a/12864196

    def reset(self):
        self._parent_map = {}
        self._parent = None

    def trace_path(self):
        x, y = self._parent
        self.grid.update_box(x, y, Locations.END)

        if self._parent == self.grid.start:
            self._state = State.RESET
            return False

        self._parent = self._parent_map[self._parent]
        return True

    def get_edges(self, x, y):
        def check_and_add(i, j):
            if not self.grid.get_val(i, j) == Locations.WALL:
                edges.put((i, j))

        edges = queue.Queue()
        if not x == 0:
            check_and_add(x - 1, y)
        if not x == self.grid.width - 1:
            check_and_add(x + 1, y)
        if not y == 0:
            check_and_add(x, y - 1)
        if not y == self.grid.height - 1:
            check_and_add(x, y + 1)
        return edges

    def step(self):
        pass
