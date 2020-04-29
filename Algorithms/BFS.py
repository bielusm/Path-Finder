from Algorithms.Algorithm import Algorithm
import queue
import copy
from Grid.Locations import Locations
from Util.Update import update_box


class BFS(Algorithm):
    @staticmethod
    def solve(grid_container, graphics, start, end, width, height):
        grid = grid_container.GRID
        q = queue.Queue()
        x, y = start
        update_box(x, y, Locations.DISCOVERED, graphics, grid_container)
        q.put(Node((x, y), []))

        while not q.empty():
            v = q.get()

            x, y = v.pos
            if v.pos == end:
                trace_path(v, graphics, grid_container)
                return v
            edges = get_edges(x, y, grid, width, height)
            while not edges.empty():
                w = edges.get()
                i, j = w
                if not grid[i][j] == Locations.DISCOVERED:
                    history = copy.deepcopy(v.history)
                    history.append(v.pos)
                    q.put(Node((i, j), history))
                    update_box(i, j, Locations.DISCOVERED, graphics, grid_container)


def get_edges(x, y, grid, width, height):
    def check_and_add(i, j):
        if not grid[i][j] == Locations.WALL:
            edges.put((i, j))

    edges = queue.Queue()
    if not x == 0:
        check_and_add(x - 1, y)
    if not x == width - 1:
        check_and_add(x + 1, y)
    if not y == 0:
        check_and_add(x, y - 1)
    if not y == height - 1:
        check_and_add(x, y + 1)
    return edges


class Node:
    pos = None
    history = None

    def __init__(self, pos, history):
        self.pos = pos
        self.history = history


# for history calculation https://stackoverflow.com/a/48260217/12252592
def trace_path(v, graphics, grid_container):
    history = v.history
    for pos in history:
        x, y = pos
        update_box(x, y, Locations.END, graphics, grid_container)
