'''Module containing the render update and event code'''
import pygame
from path.state import State
from path.graphics import Graphics
from path.menu import UIManager
from path.grid import Grid
from path.algorithm import BFS, DFS
from path.enums import Locations, FSM

MAX_SIZE = 720
MIN_SIZE = 200


def calc_scale(width, height):
    '''Calculates the scale given the width and height'''
    min_val = min(width, height)
    max_val = max(width, height)
    scale = MAX_SIZE//max_val
    if scale*min_val < MIN_SIZE:
        scale = MIN_SIZE//min_val
    return scale


class World:
    '''A class representing the current state of the world'''

    def __init__(self, width, height):
        self._scale = calc_scale(width, height)
        self.state = State(grid_size=(width, height))
        self._grid = Grid(width, height)
        self._graphics = Graphics(width, height, self._scale)
        self.manager = UIManager(
            (width*self._scale, height * self._scale), self.state)
        self._algs = [BFS(self._grid), DFS(self._grid)]


    def change_size(self):
        '''Reinitializes all objects with new grid size'''
        width, height = self.state.context['grid_size']
        self._scale = calc_scale(width, height)
        self._grid = Grid(width, height)
        self._graphics.change_size(width, height, self._scale)
        self.manager.set_resolution((width*self._scale, height * self._scale))
        self._algs = [BFS(self._grid), DFS(self._grid)]

    def handle_events(self):
        '''Handles windows and pygame events'''
        for event in pygame.event.get():
            e_type = event.type
            if e_type == pygame.QUIT:
                return False

            menu_clicked = self.manager.process_events(event)

            if not menu_clicked:
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
                        if lclick:
                            self._grid.update_box(
                                x // self._scale,
                                y // self._scale,
                                self.state.context["current_tile"])
                        if rclick:
                            self._grid.update_box(
                                x // self._scale,
                                y // self._scale,
                                Locations.EMPTY)
        return True

    def update(self, time_delta):
        '''Updates the current state of the world'''
        self.manager.update(time_delta)
        if self.state.curr == FSM.RESET:
            self._grid.reset()
            self._algs[self.state.context["alg"]].reset()
            self.state.curr = FSM.WAIT
        elif self.state.curr == FSM.RUN:
            self._grid.reset()
            self._algs[self.state.context["alg"]].reset()
            self.state.curr = FSM.RUNNING
        elif self.state.curr == FSM.RUNNING:
            if not self._algs[self.state.context["alg"]].step():
                self.state.curr = FSM.WAIT
        elif self.state.curr == FSM.SAVE:
            self._grid.save_to_file(self.state.context["map"])
            self.state.curr = FSM.WAIT
        elif self.state.curr == FSM.LOAD:
            self._grid.load_from_file(self.state.context["map"])
            self.state.curr = FSM.RESET
        elif self.state.curr == FSM.CHANGE_SIZE:
            self.change_size()
            self.state.curr = FSM.WAIT

    def draw(self):
        '''Draws everything in the world'''
        self._graphics.screen.fill((0, 0, 0))
        self._grid.draw(self._graphics)
        self.manager.draw(self._graphics.screen)
        pygame.display.flip()
