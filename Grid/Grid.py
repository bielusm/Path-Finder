from Grid.Locations import Locations


class GridContainer:
    GRID = []
    __WIDTH = 0
    __HEIGHT = 0
    __START = (0, 0)
    __END = (0, 0)

    def __init__(self, width, height, start, end):
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__START = start
        self.__END = end
        self.init_grid()

    def reset_grid(self):
        for i in range(self.__WIDTH):
            for j in range(self.__HEIGHT):
                if i == self.__END[0] and j == self.__END[1]:
                    self.GRID[i][j] = Locations.END
                elif i == self.__START[0] and j == self.__START[1]:
                    self.GRID[i][j] = Locations.START
                elif not self.GRID[i][j] == Locations.WALL:
                    self.GRID[i][j] = Locations.EMPTY

    def init_grid(self):
        self.GRID = []
        for i in range(self.__WIDTH):
            x = []
            for j in range(self.__HEIGHT):
                if i == self.__END[0] and j == self.__END[1]:
                    x.append(Locations.END)
                elif i == self.__START[0] and j == self.__START[1]:
                    x.append(Locations.START)
                else:
                    x.append(Locations.EMPTY)
            self.GRID.append(x)

    def update_box(self, x, y, val):
        self.GRID[x][y] = val
