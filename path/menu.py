'''The menu interface in the simulation'''
import pygame
from pygame import Surface


class Button:
    '''A simple button class'''
    _padding = 10

    def __init__(self, pos, text, function):
        self.pos = pos
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
        '''Checks if the user has clicked the button and calls a function if so'''
        if self._surface.get_rect().collidepoint(x - self.pos[0], y - self.pos[1]):
            self._function()
            return True
        return False

    def draw(self, graphics, offset):
        '''Draws the button'''
        x, y = self.pos
        x_offset, y_offset = offset
        graphics.draw_surface(self._surface, (x + x_offset, y + y_offset))


class RadioButton(Button):
    '''A radiobutton to select different values'''
    def __init__(self, pos, text, function, val):
        super().__init__(pos, text, function)
        self._val = val

    def click(self, x, y):
        if self._surface.get_rect().collidepoint(x - self.pos[0], y - self.pos[1]):
            self._function(self._val)


class Menu:
    '''The menu UI'''
    def __init__(self, screen_size, state):
        self.state = state
        self.width, self.height = (200, 200)
        self.pos = (screen_size[0]-self.width, screen_size[1]-self.width)
        self.menu = pygame.Surface((self.width, self.height))
        self.menu.set_alpha(100)
        self.menu.fill(pygame.Color(255, 0, 255))
        self._buttons = self.add_buttons()


    def add_buttons(self):
        '''Creates and returns a list of all the buttons in the menu'''
        buttons = []
        button = Button((0, 0), 'Start', self.start_running)
        buttons.append(button)
        button = Button((0, 40), 'Reset', self.reset)
        buttons.append(button)
        button = RadioButton((100, 0), 'BFS', self.change_alg, 0)
        buttons.append(button)
        button = RadioButton((100, 40), 'DFS', self.change_alg, 1)
        buttons.append(button)
        return buttons

    def reset(self):
        '''Sets the reset state to true'''
        self.state["reset"] = True

    def start_running(self):
        '''Sets the running state to true'''
        self.state["running"] = True

    def change_alg(self, alg):
        '''Changes the alg state to the given alg number'''
        self.state["alg"] = alg

    def button_click(self, x, y):
        '''
        Checks all buttons in the menu and
        calls their click method to see if they were clicked
        '''
        offset_x, offset_y = self.pos
        for button in self._buttons:
            if button.click(x - offset_x, y - offset_y):
                return True
        return False

    def draw(self, graphics):
        '''Draws the menu'''
        graphics.draw_surface(self.menu, self.pos)    
        for button in self._buttons:
            button.draw(graphics, self.pos)
