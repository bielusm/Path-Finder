from Algorithms.Algorithm import Algorithm
import queue
from Grid.Locations import Locations
from Util.Update import update_box
from Algorithms.Util import get_edges, trace_path
import time

# Parent Map from
# https://stackoverflow.com/a/12864196


class BFS(Algorithm):
    @staticmethod
    def solve(grid_container, graphics, start, end, width, height):
        grid = grid_container.GRID
        q = queue.Queue()
        x, y = start
        update_box(x, y, Locations.DISCOVERED, graphics, grid_container)
        q.put(start)
        parent_map = {}
        while not q.empty():
            time.sleep(0.003)
            v = q.get()
            x, y = v
            if v == end:
                trace_path(parent_map, graphics, grid_container, start, end)
                return
            edges = get_edges(x, y, grid, width, height)
            while not edges.empty():
                w = edges.get()
                i, j = w
                if not grid[i][j] == Locations.DISCOVERED:
                    parent_map[w] = v
                    q.put(w)
                    update_box(i, j, Locations.DISCOVERED, graphics, grid_container)
