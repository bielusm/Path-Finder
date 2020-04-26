# main event loop adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
# Scale adapted from https://www.youtube.com/watch?v=alhpH6ECFvQ&t=1556s&ab_channel=TheCodingTrain

import queue
import copy
import pygame

from Graphics import Graphics
from Grid import Grid

SCALE = 10
WIDTH = 64
HEIGHT = 64

MENU_BUFFER = 27

START = (2, 28)
END = (62, 32)

GridContainer = Grid.GridContainer(WIDTH, HEIGHT, START, END)

Locations = Grid.Locations


def get_edges(x, y):
    GRID = GridContainer.GRID

    def check_and_add(i, j):
        if not GRID[i][j] == Locations.WALL:
            edges.put((i, j))

    edges = queue.Queue()
    if not x == 0:
        check_and_add(x - 1, y)
    if not x == WIDTH - 1:
        check_and_add(x + 1, y)
    if not y == 0:
        check_and_add(x, y - 1)
    if not y == HEIGHT - 1:
        check_and_add(x, y + 1)
    return edges


class Node:
    pos = None
    history = None

    def __init__(self, pos, history):
        self.pos = pos
        self.history = history


def trace_path(v, graphics):
    history = v.history
    for pos in history:
        x, y = pos
        update_box(x, y, Locations.END, graphics)


# for history calculation https://stackoverflow.com/a/48260217/12252592
def breadth_first_search(graphics):
    GRID = GridContainer.GRID
    q = queue.Queue()
    x, y = START
    update_box(x, y, Locations.DISCOVERED, graphics)
    q.put(Node((x, y), []))

    while not q.empty():
        v = q.get()

        x, y = v.pos
        if v.pos == END:
            trace_path(v, graphics)
            return v
        edges = get_edges(x, y)
        while not edges.empty():
            w = edges.get()
            i, j = w
            if not GRID[i][j] == Locations.DISCOVERED:
                history = copy.deepcopy(v.history)
                history.append(v.pos)
                q.put(Node((i, j), history))
                update_box(i, j, Locations.DISCOVERED, graphics)


def update_box(x, y, val, graphics):
    GridContainer.update_box(x,y,val)
    graphics.draw_box(x, y, val)
    pygame.display.flip()


def start(graphics):
    breadth_first_search(graphics)


def reset(graphics):
    GridContainer.init_grid()
    graphics.draw_grid(GridContainer.GRID)


def main():
    graphics = Graphics.Graphics(WIDTH, HEIGHT, SCALE, MENU_BUFFER, start, reset)
    GridContainer.init_grid()
    graphics.draw_grid(GridContainer.GRID)
    running = True
    # graphics.draw_grid(GRID)
    while running:
        # Event Loop
        for event in pygame.event.get():
            e_type = event.type
            if e_type == pygame.QUIT:
                running = False
            elif e_type == pygame.MOUSEBUTTONDOWN or e_type == pygame.MOUSEBUTTONUP or e_type == pygame.MOUSEMOTION:
                x, y = event.pos
                pressed = None
                if e_type == pygame.MOUSEMOTION:
                    pressed = event.buttons[0]
                elif e_type == pygame.MOUSEBUTTONUP:
                    pressed = 0 if event.button == 1 else None
                elif e_type == pygame.MOUSEBUTTONDOWN:
                    pressed = 1 if event.button == 1 else None

                if pressed:
                    update_box(x // SCALE, (y - MENU_BUFFER) // SCALE, Locations.WALL, graphics)

        graphics.update(event)


main()
