from Util.Update import update_box
from Grid.Locations import Locations
import queue


def trace_path(parent_map, graphics, grid_container, start, end):
    parent = parent_map[end]
    while True:
        x, y = parent
        update_box(x, y, Locations.END, graphics, grid_container)

        if parent == start:
            break
        parent = parent_map[parent]


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
