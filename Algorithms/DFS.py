from Algorithms.Algorithm import Algorithm, State
from Grid.Locations import Locations
import queue

# Parent Map from
# https://stackoverflow.com/a/12864196


class DFS(Algorithm):
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
        elif self._state == State.SOLVING:
            if not self._s.empty():
                v = self._s.get()
                x, y = v
                if self.grid.get_val(x, y) == Locations.END:
                    self._parent = self.grid.end
                    self._state = State.TRACING
                    return True
                if self.grid.get_val(x, y) != Locations.DISCOVERED:
                    self.grid.update_box(x, y, Locations.DISCOVERED)
                    edges = self.get_edges(x, y)
                    while not edges.empty():
                        w = edges.get()
                        i, j = w
                        if self.grid.get_val(i, j) != Locations.DISCOVERED:
                            self._s.put(w)
                            self._parent_map[w] = v
            return True
