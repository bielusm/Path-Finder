'''The menu interface of the simulation'''
import pygame_gui
import pygame
from path.enums import FSM, Algorithms, Locations

MENU_SIZE = (195, 300)


class UIManager:
    '''Container for the UI interface'''

    def __init__(self, screen_size, state):
        self.state = state
        self._manager = pygame_gui.UIManager(screen_size, 'theme.json')
        screen_width, screen_height = screen_size
        menu_width, menu_height = MENU_SIZE
        self.ui_window = pygame_gui.elements.ui_window.UIWindow(
            rect=pygame.Rect(
                (screen_width - menu_width, screen_height - menu_height),
                (menu_width, menu_height)),
            manager=self._manager)

        window_container = self.ui_window.get_container()
        start_rect = pygame.Rect((0, 0), (50, 30))
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=start_rect,
            text='Start',
            manager=self._manager,
            container=window_container)

        reset_rect = pygame.Rect((start_rect.right, 0), (50, 30))
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=reset_rect,
            text='Reset',
            manager=self._manager,
            container=window_container)

        alg_label_rect = pygame.Rect((0, 0), (88, 20))
        alg_label_rect.centery = reset_rect.bottom + 20
        pygame_gui.elements.UILabel(
            text='Algorithm: ',
            relative_rect=alg_label_rect,
            container=window_container,
            manager=self._manager
        )

        alg_rect = pygame.Rect((95, reset_rect.bottom + 5), (50, 30))

        self.algorithm_drop_down = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            relative_rect=alg_rect,
            starting_option=Algorithms.BFS.name,
            options_list=[Algorithms.BFS.name, Algorithms.DFS.name],
            manager=self._manager,
            container=window_container,
        )

        tile_label_rect = pygame.Rect((0, 0), (48, 20))
        tile_label_rect.centery = alg_rect.bottom + 20
        pygame_gui.elements.UILabel(
            text='Tile: ',
            relative_rect=tile_label_rect,
            container=window_container,
            manager=self._manager
        )

        tile_rect = pygame.Rect((95, alg_rect.bottom+5), (65, 30))
        self.tile_drop_down = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            relative_rect=tile_rect,
            starting_option=Locations.WALL.name,
            options_list=[Locations.WALL.name,
                          Locations.START.name, Locations.END.name],
            manager=self._manager,
            container=window_container)

        save_btn_rect = pygame.Rect((0, tile_rect.bottom+5), (80, 30))
        self.save_map_button = pygame_gui.elements.UIButton(
            relative_rect=save_btn_rect,
            text='Save Map',
            manager=self._manager,
            container=window_container)

        load_btn_rect = pygame.Rect(
            (save_btn_rect.right, tile_rect.bottom+5), (80, 30))
        self.load_map_button = pygame_gui.elements.UIButton(
            relative_rect=load_btn_rect,
            text='Load Map',
            manager=self._manager,
            container=window_container)

        map_drop_down_rect = pygame.Rect((0, load_btn_rect.bottom), (80, 30))
        self.map_drop_down = pygame_gui.elements.UIDropDownMenu(
            relative_rect=map_drop_down_rect,
            starting_option='Map 0',
            options_list=['Map 0', 'Map 1', 'Map 2'],
            manager=self._manager,
            container=window_container)

        grid_rect = pygame.Rect((0, map_drop_down_rect.bottom + 5), (40, 0))
        self.grid_text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=grid_rect,
            manager=self._manager,
            container=self.ui_window
        )
        self.grid_text_entry.set_allowed_characters('numbers')
        self.grid_text_entry.set_text_length_limit(3)

        grid_button_rect = pygame.Rect(
            (grid_rect.right+5, map_drop_down_rect.bottom + 5),
            (75, 30))
        self.grid_button = pygame_gui.elements.UIButton(
            relative_rect=grid_button_rect,
            text='Set Grid',
            manager=self._manager,
            container=window_container)

        speed_slider_rect = pygame.Rect(
            (0, grid_button_rect.bottom),
            (100, 20))
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=speed_slider_rect,
            start_value=50,
            value_range=[1, 100],
            manager=self._manager,
            container=window_container
        )

        # Doesen't let the user click the grid if they're clicking on the menu
        self.blocking = False

    def set_resolution(self, size):
        '''Passes a size tuple to the manager to change the resolution'''
        self._manager.set_window_resolution(size)

    def handle_button_event(self, event):
        '''Handles all button events'''
        if event.ui_element == self.start_button:
            self.start_running()
        elif event.ui_element == self.reset_button:
            self.reset()
        elif event.ui_element == self.save_map_button:
            self.save_map()
        elif event.ui_element == self.load_map_button:
            self.load_map()
        elif event.ui_element == self.grid_button:
            self.set_grid_size()

    def handle_drop_down_event(self, event):
        '''handles all drop down events'''
        text = event.text
        if event.ui_element == self.algorithm_drop_down:
            self.change_alg(text)
        elif event.ui_element == self.tile_drop_down:
            self.change_tile(text)
        elif event.ui_element == self.map_drop_down:
            self.change_map(text)

    def handle_slider_event(self, event):
        '''handles all horizontal slider events'''
        value = event.value
        if event.ui_element == self.speed_slider:
            self.change_speed(value)

    def process_events(self, event):
        '''Handle all events for the menu'''
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.handle_button_event(event)
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                self.handle_drop_down_event(event)
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self.handle_slider_event(event)

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

    def change_speed(self, value):
        '''Changes speed state to given value'''
        self.state.context["speed"] = value

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

    def set_grid_size(self):
        '''Sets EITHER x or y in the grid_size tuple'''
        x = self.grid_text_entry.get_text()
        if x:
            x = (int(x))
            if 3 <= x <= 100:
                self.state.context["grid_size"] = (int(x), int(x))
                self.state.curr = FSM.CHANGE_SIZE

    def change_tile(self, text):
        '''Changes the tile_text based on the given value'''
        self.state.context["current_tile"] = Locations[text]
