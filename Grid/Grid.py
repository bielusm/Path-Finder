from Grid.Locations import Locations


class Grid:
    class Cell:
        def __init__(self, val):
            self.val = val
            self.changed = True

        def set_val(self, val):
            self.val = val
            self.changed = True

    _grid = []
    width = 0
    height = 0
    start = (0, 1)
    end = (19, 15)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init_grid()

    def get_val(self, x, y):
        return self._grid[x][y].val

    def reset(self):
        for i in range(self.width):
            for j in range(self.height):
                self._grid[i][j].changed = True
                if i == self.end[0] and j == self.end[1]:
                    self._grid[i][j].val = Locations.END
                elif i == self.start[0] and j == self.start[1]:
                    self._grid[i][j].val = Locations.START
                elif not self._grid[i][j].val == Locations.WALL:
                    self._grid[i][j].val = Locations.EMPTY
                else:
                    self._grid[i][j].changed = False

    def init_grid(self):
        self._grid = []
        for i in range(self.width):
            x = []
            for j in range(self.height):
                if i == self.end[0] and j == self.end[1]:
                    x.append(self.Cell(Locations.END))
                elif i == self.start[0] and j == self.start[1]:
                    x.append(self.Cell(Locations.START))
                else:
                    x.append(self.Cell(Locations.EMPTY))
            self._grid.append(x)

    def update_box(self, x, y, val):
        self._grid[x][y].set_val(val)

    @staticmethod
    def draw_box(x, y, val, graphics):
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
        graphics.draw_cell(x, y, color)

    def draw(self, graphics):
        for x in range(self.width):
            for y in range(self.height):
                curr = self._grid[x][y]
                if curr.changed:
                    self.draw_box(x, y, curr.val, graphics)
                    curr.changed = False
