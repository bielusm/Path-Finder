'''All of the drawing classes'''
import pygame
from pygame import DOUBLEBUF

class Graphics:
    '''Various methods for drawing things on screen'''
    def __init__(self, width, height, scale):
        self._width = width
        self._height = height
        self._scale = scale
        pygame.init()
        self.screen = pygame.display.set_mode([width * scale, height * scale], DOUBLEBUF)
        # For speed
        self.screen.set_alpha(None)

    def draw_cell(self, x, y, color):
        '''Draws a grid cell in a specified location with a specified color'''
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(x * self._scale,
                        y * self._scale,
                        self._scale - 1,
                        self._scale - 1))

    def draw_surface(self, surface, pos):
        '''Draws a pygame surface on the main screen'''
        self.screen.blit(surface, pos)
