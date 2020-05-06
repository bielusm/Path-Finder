import pygame
from pygame import *


class Button:
    _padding = 10

    def __init__(self, pos, text, function):
        self._pos = pos
        self._function = function
        self._default_font = pygame.font.Font(
            pygame.font.get_default_font(), 20)
        text_surface = self._default_font.render(text, True, (0, 0, 0))
        self._surface = Surface((text_surface.get_width(
        ) + self._padding, text_surface.get_height() + self._padding))
        self._surface.fill((255, 255, 255))
        self._surface.blit(
            text_surface, (self._padding // 2, self._padding // 2))

    def click(self, x, y):
        print(self._surface.get_rect())
        if self._surface.get_rect().collidepoint(x - self._pos[0], y - self._pos[1]):
            self._function()
            print("click button")
            return True

    def draw(self, graphics, offset):
        x, y = self._pos
        x_offset, y_offset = offset
        graphics.draw_surface(self._surface, (x + x_offset, y + y_offset))


class RadioButton(Button):
    def __init__(self, pos, text, function, val):
        super().__init__(pos, text, function)
        self._val = val

    def click(self, x, y):
        if self._surface.get_rect().collidepoint(x - self._pos[0], y - self._pos[1]):
            print("click radiobutton")
            self._function(self._val)


class Menu:
    def __init__(self, size, pos, state):
        self.state = state
        self.start = False
        self.alg = 0

        self.width, self.height = size
        self._pos = pos
        self._menu = pygame.Surface((self.width, self.height))
        self._menu.set_alpha(50)
        self._menu.fill(pygame.Color(255, 0, 255))
        self._buttons = []
        button = Button((0, 0), 'Start', self.start_running)
        self._buttons.append(button)
        button = RadioButton((100, 0), 'BFS', self.change_alg, 0)
        self._buttons.append(button)
        button = RadioButton((100, 40), 'DFS', self.change_alg, 1)
        self._buttons.append(button)

    def start_running(self):
        self.state.running = True

    def change_alg(self, alg):
        self.state.alg = alg

    def button_click(self, x, y):
        offset_x, offset_y = self._pos
        for button in self._buttons:
            if button.click(x - offset_x, y - offset_y):
                return True

    def draw(self, graphics):
        graphics.draw_surface(self._menu, self._pos)
        for button in self._buttons:
            button.draw(graphics, self._pos)