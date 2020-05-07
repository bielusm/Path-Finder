'''Module for Depth First Search Algorithm'''
import queue
from algorithms.algorithm import Algorithm, State
from grid.locations import Locations

# Parent Map from
# https://stackoverflow.com/a/12864196


class DFS(Algorithm):
    '''DFS Class'''
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
        if self._state == State.RESET:
            self.reset()
            return True
        elif self._state == State.TRACING:
            return self.trace_path()
        else:
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
