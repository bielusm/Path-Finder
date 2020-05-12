'''The menu interface in the simulation'''
import pygame
from pygame import Surface
from path.grid import Locations

class Button:
    '''A simple button class'''
    _padding = 20

    def __init__(self, pos, text, color, function):
        self.pos = pos
        self._function = function
        if text:
            self._surface = self.create_text_surface(text)
        else:
            self._surface = self.create_rect_surface(color)

    def create_rect_surface(self, color):
        '''Creates a rect surface and fills it with color'''
        surface = Surface((self._padding, self._padding))
        surface.fill(color)
        return surface

    def create_text_surface(self, text):
        '''Creates a text surface with a white background'''
        self._default_font = pygame.font.Font(
            pygame.font.get_default_font(), 14)
        text_surface = self._default_font.render(text, True, (0, 0, 0))
        surface = Surface((text_surface.get_width(
        ) + self._padding, text_surface.get_height() + self._padding))
        surface.fill((255, 255, 255))
        surface.blit(
            text_surface, (self._padding // 2, self._padding // 2))
        return surface

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


class RadioButtonContainer():
    '''Container for radio buttons'''
    def __init__(self):
        super().__init__()
        self._buttons = []
        self._selected = 0

    def add_button(self, pos, text, color, function, val):
        '''Add radio button to the list'''
        self._buttons.append(RadioButton(pos, text, color, function, val))

    def click(self, x, y):
        '''Check click for radio buttons'''
        for index, button in enumerate(self._buttons):
            if button.click(x, y):
                self._selected = index
                return True
        return False

    def draw(self, graphics, offset):
        '''Calls the draw method for each button'''
        for index, button in enumerate(self._buttons):
            selected = index == self._selected
            button.draw_self(graphics, offset, selected)

class RadioButton(Button):
    '''A radiobutton to select different values'''
    def __init__(self, pos, text, color, function, val):
        super().__init__(pos, text, color, function)
        self._val = val

    def click(self, x, y):
        if self._surface.get_rect().collidepoint(x - self.pos[0], y - self.pos[1]):
            self._function(self._val)
            return True
        return False

    def draw_self(self, graphics, offset, selected):
        '''Draws itself'''
        x, y = self.pos
        x_offset, y_offset = offset
        if selected:
            outline_surface = Surface(
                (self._surface.get_width() + 2, self._surface.get_height() + 2))
            outline_surface.fill((0, 0, 0))
            outline_surface.blit(self._surface, (1, 1))
            graphics.draw_surface(outline_surface, (x + x_offset, y + y_offset))
        else:
            graphics.draw_surface(self._surface, (x + x_offset, y + y_offset))

class Menu:
    '''Creates the Menu on screen'''
    tile_text_pos = (10, 100)
    menu_size = (190, 200)
    '''The menu UI'''
    def __init__(self, screen_size, state):
        self.state = state
        self.width, self.height = self.menu_size
        self.pos = (screen_size[0]-self.width, screen_size[1]-self.height)
        self.menu = pygame.Surface((self.width, self.height))
        self._tile_text = "Wall"
        self._buttons = self.add_buttons()

    def add_buttons(self):
        '''Creates and returns a list of all the buttons in the menu'''
        buttons = []
        buttons.append(Button((0, 0), 'Start', None, self.start_running))
        buttons.append(Button((0, 40), 'Reset', None, self.reset))
        alg_radio_container = RadioButtonContainer()
        alg_radio_container.add_button((100, 0), 'BFS', None, self.change_alg, 0)
        alg_radio_container.add_button((100, 40), 'DFS', None, self.change_alg, 1)
        buttons.append(alg_radio_container)
        tile_container = RadioButtonContainer()
        tile_container.add_button((10, 100), None, (255, 255, 0), self.change_tile, Locations.START)
        tile_container.add_button((40, 100), None, (0, 255, 0), self.change_tile, Locations.END)
        tile_container.add_button((70, 100), None, (0, 0, 0), self.change_tile, Locations.WALL)
        buttons.append(tile_container)
        buttons.append(Button((0, 130), 'Load Map', None, self.load_map))
        buttons.append(Button((100, 130), 'Save Map', None, self.save_map))
        return buttons

    def load_map(self):
        '''Will load a map from file'''

    def save_map(self):
        '''Will saves a map to file'''

    def change_tile(self, val):
        '''Changes the tile_text based on the given value'''
        self.state["current_tile"] = val
        if val == Locations.START:
            self._tile_text = "Start"
        elif val == Locations.END:
            self._tile_text = "End"
        else:
            self._tile_text = "Wall"


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
        menu_clicked = self.menu.get_rect().collidepoint(x- offset_x, y - offset_y)
        for button in self._buttons:
            if button.click(x - offset_x, y - offset_y):
                break
        return menu_clicked

    def draw(self, graphics):
        '''Draws the menu'''
        self.menu.fill(pygame.Color(200, 200, 200))
        graphics.draw_surface(self.menu, self.pos)
        for button in self._buttons:
            button.draw(graphics, self.pos)
