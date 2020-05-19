'''The menu interface of the simulation'''
import pygame_gui
import pygame
from path.enums import FSM, Algorithms, Locations

class UIManager:
    '''Container for the UI interface'''
    def __init__(self, screen_size, state):
        self.state = state
        self._manager = pygame_gui.UIManager(screen_size, 'theme.json')
        self.ui_window = pygame_gui.elements.ui_window.UIWindow(
            rect=pygame.Rect((50, 50), (200, 300)),
            manager=self._manager)
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (50, 50)),
            text='Start',
            manager=self._manager,
            container=self.ui_window)

        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 0), (50, 50)),
            text='Reset',
            manager=self._manager,
            container=self.ui_window)

        self.algorithm_drop_down = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            relative_rect=pygame.Rect((0, 50), (60, 30)),
            starting_option=Algorithms.BFS.name,
            options_list=[Algorithms.BFS.name, Algorithms.DFS.name],
            manager=self._manager,
            container=self.ui_window)

        self.tile_drop_down = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            relative_rect=pygame.Rect((60, 50), (80, 30)),
            starting_option=Locations.WALL.name,
            options_list=[Locations.WALL.name, Locations.START.name, Locations.END.name],
            manager=self._manager,
            container=self.ui_window)

        self.save_map_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 80), (80, 30)),
            text='Save Map',
            manager=self._manager,
            container=self.ui_window)

        self.load_map_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((80, 80), (80, 30)),
            text='Load Map',
            manager=self._manager,
            container=self.ui_window)


        self.map_drop_down = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            relative_rect=pygame.Rect((0, 110), (80, 30)),
            starting_option='Map 0',
            options_list=['Map 0', 'Map 1', 'Map 2'],
            manager=self._manager,
            container=self.ui_window)



        self.blocking = False






    def process_events(self, event):
        '''Handle all events for the menu'''
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.start_running()
                elif event.ui_element == self.reset_button:
                    self.reset()
                elif event.ui_element == self.save_map_button:
                    self.save_map()
                elif event.ui_element == self.load_map_button:
                    self.load_map()
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                text = event.text
                if event.ui_element == self.algorithm_drop_down:
                    self.change_alg(text)
                elif event.ui_element == self.tile_drop_down:
                    self.change_tile(text)
                elif event.ui_element == self.map_drop_down:
                    self.change_map(text)




        # This check makes it so the grid will be disabled when the user clicks on the menu
        elif (event.type == pygame.MOUSEBUTTONDOWN
              and self.ui_window.check_clicked_inside_or_blocking(event)):
            self.blocking = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.blocking = False
        self._manager.process_events(event)
        return self.blocking



    def update(self, time_delta):
        '''Runs manager update function'''
        self._manager.update(time_delta)

    def draw(self, windows_surface):
        '''Runs manager draw ui function'''
        self._manager.draw_ui(windows_surface)

    def change_alg(self, text):
        '''Changes the alg state to the given alg number'''
        self.state.context["alg"] = Algorithms[text]
        self.state.curr = FSM.RESET

    def start_running(self):
        '''Sets program state to run'''
        self.state.curr = FSM.RUN

    def reset(self):
        '''Sets program state to reset'''
        self.state.curr = FSM.RESET

    def change_map(self, text):
        '''Changes map variable'''
        if(text) == 'Map 0':
            val = 0
        elif(text) == 'Map 1':
            val = 1
        else:
            val = 2
        self.state.context["map"] = val

    def load_map(self):
        '''Sets program state to load'''
        self.state.curr = FSM.LOAD

    def save_map(self):
        '''Sets program state to save'''
        self.state.curr = FSM.SAVE

    def change_tile(self, text):
        '''Changes the tile_text based on the given value'''
        self.state.context["current_tile"] = Locations[text]
