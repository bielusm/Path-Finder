
'''The main grid module'''
from queue import LifoQueue
from path.enums import Locations

class Grid:
    '''Holds a grid of cells that represent the maze'''
    class Cell:
        '''Each cell of the grid'''
        def __init__(self, val):
            self.val = val
            self.changed = True

        def set_val(self, val):
            '''Changes the val of the grid and sets itself to changed for drawing efficency'''
            self.val = val
            self.changed = True

    _grid = []
    width = 0
    height = 0
    start = None
    end = None
    _active_discoveries = LifoQueue()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init_grid()

    def get_val(self, x, y):
        '''Gets a grid val at x, y coordinates'''
        return self._grid[x][y].val

    def reset(self):
        '''Resets the grid to initial values, does not reset walls'''
        for i in range(self.width):
            for j in range(self.height):
                self._grid[i][j].changed = True
                if self.end and i == self.end[0] and j == self.end[1]:
                    self._grid[i][j].val = Locations.END
                elif self.start and i == self.start[0] and j == self.start[1]:
                    self._grid[i][j].val = Locations.START
                elif not self._grid[i][j].val == Locations.WALL:
                    self._grid[i][j].val = Locations.EMPTY
                else:
                    self._grid[i][j].changed = False

    def init_grid(self):
        '''Initializes an empty grid'''
        self._grid = []
        for i in range(self.width):
            x = []
            for j in range(self.height):
                if self.end and i == self.end[0] and j == self.end[1]:
                    x.append(self.Cell(Locations.END))
                elif self.start and i == self.start[0] and j == self.start[1]:
                    x.append(self.Cell(Locations.START))
                else:
                    x.append(self.Cell(Locations.EMPTY))
            self._grid.append(x)

    def update_box(self, x, y, val):
        '''Changes the value of a grid cell at an x, y coordinate'''

        # This check is nessicary so only the user can override start and end values
        if val != Locations.DISCOVERED and val != Locations.PATH:
            curr_val = self._grid[x][y].val
            if curr_val == Locations.START:
                self.start = None
            if curr_val == Locations.END:
                self.end = None

        if val == Locations.END:
            if self.end:
                i, j = self.end
                self._grid[i][j].set_val(Locations.EMPTY)
            self._grid[x][y].set_val(Locations.END)
            self.end = (x, y)
        elif val == Locations.START:
            if self.start:
                i, j = self.start
                self._grid[i][j].set_val(Locations.EMPTY)
            self._grid[x][y].set_val(Locations.START)
            self.start = (x, y)
        elif val == Locations.DISCOVERED:
            self._grid[x][y].set_val(Locations.DISCOVERED)
            self._active_discoveries.put((x, y))

        else:
            self._grid[x][y].set_val(val)


    def draw(self, graphics):
        '''Draws each cell in the grid'''
        def draw_box(x, y, val, graphics):
            if val == Locations.START:
                color = (255, 0, 0)
            elif val in [Locations.END, Locations.PATH, Locations.ACTIVE]:
                color = (0, 255, 0)
            elif val == Locations.EMPTY:
                color = (255, 255, 255)
            elif val == Locations.WALL:
                color = (0, 0, 0)
            else:  # val == Locations.DISCOVERED:
                color = (255, 255, 0)
            graphics.draw_cell(x, y, color)

        for x in range(self.width):
            for y in range(self.height):
                curr = self._grid[x][y]
                draw_box(x, y, curr.val, graphics)
                curr.changed = False

        # Highlight newest discoveries
        while not self._active_discoveries.empty():
            pos = self._active_discoveries.get()
            x, y = pos
            draw_box(x, y, Locations.ACTIVE, graphics)
            self._grid[x][y].changed = True

    def save_to_file(self, num):
        '''Saves the current grid to a txt file'''
        self.reset()
        file = open(f'grid{num}.txt', 'w', buffering=1)
        for j in range(self.height):
            for i in range(self.width):
                file.write(str(self._grid[i][j].val.value))
            file.write('\n')
        print(f'File grid{num} written')
        file.close()

    def load_from_file(self, num):
        '''Loads current grid from file'''
        try:
            file = open(f'grid{num}.txt', 'r', buffering=1)
            for j in range(self.height):
                line = file.readline().rstrip()
                for i, val in enumerate(line):
                    val = Locations(int(val))
                    self.update_box(i, j, val)
            print("File loaded")
        except FileNotFoundError:
            print("File not found")
