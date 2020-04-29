import pygame
from Grid.Locations import Locations


class Graphics:
    __screen = None
    __WIDTH = 0
    __HEIGHT = 0
    __SCALE = 0

    def __init__(self, width, height, scale):
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__SCALE = scale
        pygame.init()
        self.__screen = pygame.display.set_mode([width * scale, height * scale])

    def draw_box(self, x, y, val):
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

        pygame.draw.rect(
            self.__screen,
            color,
            pygame.Rect(x * self.__SCALE,
                        y * self.__SCALE,
                        self.__SCALE - 1,
                        self.__SCALE - 1))

    def draw_grid(self, grid):
        for x in range(self.__WIDTH):
            for y in range(self.__HEIGHT):
                self.draw_box(x, y, grid[x][y])
        pygame.display.flip()
