import pygame
from Graphics import Graphics
from Grid.Grid import Grid
from Grid import Locations
from Graphics.Menu import Menu
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS

algs = []

Locations = Locations.Locations


class State:
    running = False
    alg = 0
    reset = False


class World:
    def __init__(self, width, height, scale):
        self._state = State()
        self._width = width
        self._height = height
        self._scale = scale
        self._grid = Grid(width, height)
        self._graphics = Graphics.Graphics(width, height, scale)
        self._menu = Menu((400, 200), (width*scale-400,
                                       height*scale-200), self._state)
        self._alg = 0
        global algs
        algs = [BFS(self._grid), DFS(self._grid)]

    def handle_events(self):
        for event in pygame.event.get():
            e_type = event.type
            if e_type == pygame.QUIT:
                return False
            if e_type == pygame.MOUSEBUTTONDOWN or e_type == pygame.MOUSEBUTTONUP or e_type == pygame.MOUSEMOTION:
                x, y = event.pos
                lclick = None
                rclick = None
                if e_type == pygame.MOUSEMOTION:
                    lclick = event.buttons[0]
                    rclick = event.buttons[2]
                elif e_type == pygame.MOUSEBUTTONUP:
                    lclick = 0 if event.button == 1 else None
                    rclick = 0 if event.button == 3 else None
                elif e_type == pygame.MOUSEBUTTONDOWN:
                    lclick = 1 if event.button == 1 else None
                    rclick = 1 if event.button == 3 else None

                if lclick or rclick:
                    if not self._menu.button_click(x, y):
                        if lclick:
                            self._grid.update_box(
                                x // self._scale, y // self._scale, Locations.WALL)
                        if rclick:
                            self._grid.update_box(
                                x // self._scale, y // self._scale, Locations.EMPTY)
        return True

    def update(self):
        if self._state.reset:
            self._state.reset = False
            self._grid.reset()
        elif self._state.running:
            if algs[self._state.alg]:
                self._state.running = algs[self._state.alg].step()

    def draw(self):
        self._grid.draw(self._graphics)
        self._menu.draw(self._graphics)
        pygame.display.flip()
