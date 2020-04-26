# main event loop adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
# Scale adapted from https://www.youtube.com/watch?v=alhpH6ECFvQ&t=1556s&ab_channel=TheCodingTrain

from enum import Enum
import queue
import copy
import pygame
import thorpy


class Locations(Enum):
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3
    DISCOVERED = 4


SCALE = 10
WIDTH = 64
HEIGHT = 64

MENU_BUFFER = 27

START = (2, 28)
END = (62, 32)

GRID = []


def get_edges(x, y):
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


def trace_path(v, screen):
    history = v.history
    for pos in history:
        x, y = pos
        update_box(screen, x, y, Locations.END)


# for history calculation https://stackoverflow.com/a/48260217/12252592
def breadth_first_search(screen):
    q = queue.Queue()
    x, y = START
    update_box(screen, x, y, Locations.DISCOVERED)
    q.put(Node((x, y), []))

    while not q.empty():
        v = q.get()

        x, y = v.pos
        if v.pos == END:
            trace_path(v, screen)
            return v
        edges = get_edges(x, y)
        while not edges.empty():
            w = edges.get()
            i, j = w
            if not GRID[i][j] == Locations.DISCOVERED:
                history = copy.deepcopy(v.history)
                history.append(v.pos)
                q.put(Node((i, j), history))
                update_box(screen, i, j, Locations.DISCOVERED)


def init_grid():
    global GRID
    GRID = []
    for i in range(WIDTH):
        x = []
        for j in range(HEIGHT):
            if i == END[0] and j == END[1]:
                x.append(Locations.END)
            elif i == START[0] and j == START[1]:
                x.append(Locations.START)
            else:
                x.append(Locations.EMPTY)
        GRID.append(x)


def draw_grid(screen):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            draw_box(screen, x, y, GRID[x][y])
    pygame.display.flip()


def update_box(screen, x, y, val):
    GRID[x][y] = val
    draw_box(screen, x, y, val)
    pygame.display.flip()


def draw_box(screen, x, y, val):
    if val == Locations.START:
        color = (255, 0, 0)
    elif val == Locations.END:
        color = (0, 255, 0)
    elif val == Locations.EMPTY:
        color = (255, 255, 255)
    elif val == Locations.WALL:
        color = (0, 0, 0)
    else:  # val == Locations.DISCOVERED:
        color = (255, 255, 0)

    pygame.draw.rect(screen, color, pygame.Rect(x * SCALE, MENU_BUFFER + y * SCALE, SCALE - 1, SCALE - 1))


def create_menu(screen):
    start_button = thorpy.make_button("Start", func=start, params={"screen": screen})
    start_button.set_topleft((0, 0))
    reset_button = thorpy.make_button("Reset", func=reset, params={"screen": screen})
    reset_button.set_topleft((42, 0))
    start_button.blit()
    start_button.update()
    reset_button.blit()
    reset_button.update()
    menu = thorpy.Menu([start_button, reset_button])
    return menu


def start(screen):
    breadth_first_search(screen)


def reset(screen):
    init_grid()
    draw_grid(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH * SCALE, MENU_BUFFER + HEIGHT * SCALE])
    init_grid()
    draw_grid(screen)

    running = True

    menu = create_menu(screen)

    for element in menu.get_population():
        element.surface = screen

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
                    update_box(screen, x // SCALE, (y - MENU_BUFFER) // SCALE, Locations.WALL)

            menu.react(event)


main()
