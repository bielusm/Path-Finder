import queue
from Algorithms.Algorithm import Algorithm, State
from Grid.Locations import Locations


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self._q = queue.Queue()
        self._grid = grid
        x, y = self._grid.start
        self._grid.update_box(x, y, Locations.DISCOVERED)
        self._q.put(grid.start)
        self._finished = False

    def reset(self):
        super().reset()
        self._grid.reset()
        self._q = queue.Queue()
        x, y = self._grid.start
        self._grid.update_box(x, y, Locations.DISCOVERED)
        self._q.put(self._grid.start)
        self._finished = False
        self._state = State.SOLVING

    def step(self):
        if self._state == State.RESET:
            self.reset()
            return True
        elif self._state == State.SOLVING:
            if not self._q.empty():
                v = self._q.get()
                x, y = v
                if v == self._grid.end:
                    self._state = State.TRACING
                    self._parent = self._grid.end
                    return True
                edges = self.get_edges(x, y)
                while not edges.empty():
                    w = edges.get()
                    i, j = w
                    if not self._grid.get_val(i, j) == Locations.DISCOVERED:
                        self._parent_map[w] = v
                        self._q.put(w)
                        self._grid.update_box(i, j, Locations.DISCOVERED)
            return True
        elif self._state == State.TRACING:
            self.trace_path()
            return True
