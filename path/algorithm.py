'''This module holds the basic Algorithm that Algorithms inheirt from and Holds the State Enum'''
import queue
from abc import ABC
from enum import Enum, auto
from path.enums import Locations

class State(Enum):
    '''Every State an Algorithm can be in'''
    SOLVING = auto()
    TRACING = auto()
    SOLVED = auto()
    RESET = auto()
    WAITING = auto()


class Algorithm(ABC):
    '''
    A class containing functions and members that each algorithm needs

    Parent Map from
    https://stackoverflow.com/a/12864196
    '''
    def __init__(self, grid):
        self.grid = grid
        self._state = State.RESET
        self._parent_map = {}
        self._parent = None
        # Parent Map from https://stackoverflow.com/a/12864196

    def reset(self):
        '''Resets members to initial settings'''
        self._state = State.RESET
        self._parent_map = {}
        self._parent = None
        self.grid.reset()
        if not self.grid.start or not self.grid.end:
            self._state = State.WAITING


    def trace_path(self):
        '''Updates grid step by step so a path is drawn from the end to the start'''
        row, col = self._parent
        self.grid.update_box(row, col, Locations.PATH)

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


class BFS(Algorithm):
    '''Breath First Search Algorithm'''
    def __init__(self, grid):
        super().__init__(grid)
        self._q = None


    def reset(self):
        super().reset()
        self._q = queue.Queue()

        if self._state != State.WAITING:
            x, y = self.grid.start
            self._q.put((x, y))
            self.grid.update_box(x, y, Locations.DISCOVERED)
            self._state = State.SOLVING

    def step(self):
        if self._state == State.WAITING:
            return False
        if self._state == State.RESET:
            self.reset()
            return True
        if self._state == State.SOLVING:
            if not self._q.empty():
                vertex = self._q.get()
                x, y = vertex
                if vertex == self.grid.end:
                    self._state = State.TRACING
                    self._parent = self.grid.end
                    return True
                edges = self.get_edges(x, y)
                while not edges.empty():
                    neighbor = edges.get()
                    i, j = neighbor
                    if not self.grid.get_val(i, j) == Locations.DISCOVERED:
                        self._parent_map[neighbor] = vertex
                        self._q.put(neighbor)
                        if self.grid.get_val(i, j) == Locations.END:
                            return True
                        self.grid.update_box(i, j, Locations.DISCOVERED)
            return True
        # self._state == State.TRACING:
        return self.trace_path()



class DFS(Algorithm):
    '''Depth First Search Algorithm'''
    def __init__(self, grid):
        super().__init__(grid)
        self._s = queue.LifoQueue()
        self._s.put(self.grid.start)

    def reset(self):
        super().reset()
        self.grid.reset()
        self._s = queue.LifoQueue()
        self._s.put(self.grid.start)
        self._state = State.SOLVING

    def step(self):
        if self._state == State.WAITING:
            return False
        if self._state == State.RESET:
            self.reset()
            return True
        if self._state == State.TRACING:
            return self.trace_path()

        # self._state == State.SOLVING:
        if not self._s.empty():
            vertex = self._s.get()
            x, y = vertex
            if self.grid.get_val(x, y) == Locations.END:
                self._parent = self.grid.end
                self._state = State.TRACING
                return True
            if self.grid.get_val(x, y) != Locations.DISCOVERED:
                self.grid.update_box(x, y, Locations.DISCOVERED)
                edges = self.get_edges(x, y)
                while not edges.empty():
                    edge = edges.get()
                    i, j = edge
                    if self.grid.get_val(i, j) != Locations.DISCOVERED:
                        self._s.put(edge)
                        self._parent_map[edge] = vertex
        return True
