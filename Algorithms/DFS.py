from Algorithms.Algorithm import Algorithm
from Grid.Locations import Locations
from Util.Update import update_box
from Algorithms.Util import trace_path, get_edges
import queue
import time

# Parent Map from
# https://stackoverflow.com/a/12864196


class DFS(Algorithm):
    @staticmethod
    def solve(grid_container, graphics, start, end, width, height):
        parent_map = {}
        g = grid_container.GRID
        # Stack
        s = queue.LifoQueue()
        s.put(start)
        while not s.empty():
            time.sleep(0.003)
            v = s.get()
            x, y = v
            if g[x][y] == Locations.END:
                trace_path(parent_map, graphics, grid_container, start, end)
                return
            if g[x][y] != Locations.DISCOVERED:
                update_box(x, y, Locations.DISCOVERED, graphics, grid_container)
                edges = get_edges(x, y, g, width, height)
                while not edges.empty():
                    w = edges.get()
                    i, j = w
                    if g[i][j] != Locations.DISCOVERED:
                        s.put(w)
                        parent_map[w] = v
