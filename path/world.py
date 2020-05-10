'''Module containing the render update and event code'''
import pygame

from path.graphics import Graphics
from path.menu import Menu
from path.grid import Grid, Locations
from path.algorithm import BFS, DFS

class World:
    '''A class representing the current state of the world'''
    def __init__(self, width, height, scale):
        self._state = dict(
            running=False,
            alg=0,
            reset=False,
            current_tile=Locations.WALL)
        self._width = width
        self._height = height
        self._scale = scale
        self._grid = Grid(width, height)
        self._graphics = Graphics(width, height, scale)
        self._menu = Menu((width*scale, height*scale), self._state)
        self._algs = [BFS(self._grid), DFS(self._grid)]
    def handle_events(self):
        '''Handles windows and pygame events'''
        for event in pygame.event.get():
            e_type = event.type
            if e_type == pygame.QUIT:
                return False
            if (e_type == pygame.MOUSEBUTTONDOWN
                    or e_type == pygame.MOUSEBUTTONUP
                    or e_type == pygame.MOUSEMOTION):
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
                                x // self._scale, y // self._scale, self._state["current_tile"])
                        if rclick:
                            self._grid.update_box(
                                x // self._scale, y // self._scale, Locations.EMPTY)
        return True

    def update(self):
        '''Updates the current state of the world'''
        if self._state["reset"]:
            self._state["reset"] = False
            self._grid.reset()
        elif self._state["running"]:
            if self._algs[self._state["alg"]]:
                self._state["running"] = self._algs[self._state["alg"]].step()

    def draw(self):
        '''Draws everything in the world'''

        menu_rect = self.calc_menu_rect()
        self._grid.draw(self._graphics, menu_rect)
        self._menu.draw(self._graphics)
        pygame.display.flip()

    def calc_menu_rect(self):
        '''
        Scales the menu down to grid coordinates
        and rects a rect representing where it is
        '''
        rect = self._menu.menu.get_rect()
        rect.x = self._menu.pos[0]/self._scale
        rect.y = self._menu.pos[1]/self._scale
        rect.width = rect.width / self._scale
        rect.height = rect.height / self._scale
        return rect
