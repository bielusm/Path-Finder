import pygame
import thorpy
from Grid import Grid


class Graphics:
    __screen = None
    __WIDTH = 0
    __HEIGHT = 0
    __SCALE = 0
    __MENU_BUFFER = 0
    __locations = None
    menu = None
    __start = None
    __reset = None

    def __init__(self, width, height, scale, menu_buffer, start, reset):
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__SCALE = scale
        self.__MENU_BUFFER = menu_buffer
        self.__locations = Grid.Locations
        pygame.init()
        self.__screen = pygame.display.set_mode([width * scale, menu_buffer + height * scale])
        self.__start = start
        self.__reset = reset
        self.menu = self.create_menu()
        for element in self.menu.get_population():
            element.surface = self.__screen


    def update(self, event):
        self.menu.react(event)

    def create_menu(self):
        start_button = thorpy.make_button("Start", func=self.__start, params={"graphics": self})
        start_button.set_topleft((0, 0))
        reset_button = thorpy.make_button("Reset", func=self.__reset, params={"graphics": self})
        reset_button.set_topleft((42, 0))
        start_button.blit()
        start_button.update()
        reset_button.blit()
        reset_button.update()
        menu = thorpy.Menu([start_button, reset_button])
        return menu

    def draw_box(self, x, y, val):
        if val == self.__locations.START:
            color = (255, 0, 0)
        elif val == self.__locations.END:
            color = (0, 255, 0)
        elif val == self.__locations.EMPTY:
            color = (255, 255, 255)
        elif val == self.__locations.WALL:
            color = (0, 0, 0)
        else:  # val == Locations.DISCOVERED:
            color = (255, 255, 0)

        pygame.draw.rect(
            self.__screen,
            color,
            pygame.Rect(x * self.__SCALE,
                        self.__MENU_BUFFER + y * self.__SCALE,
                        self.__SCALE - 1,
                        self.__SCALE - 1))

    def draw_grid(self, grid):
        for x in range(self.__WIDTH):
            for y in range(self.__HEIGHT):
                self.draw_box(x, y, grid[x][y])
        pygame.display.flip()
