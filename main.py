# main event loop adapted from https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html

import pygame
from tkinter import *
from tkinter import ttk
import os
from Graphics import Graphics
from Grid import Grid
from Grid import Locations
from Algorithms import BFS
from Util import Update
update_box = Update.update_box

SCALE = 10
WIDTH = 64
HEIGHT = 64


START = (2, 28)
END = (62, 32)

RUNNING = True

GridContainer = Grid.GridContainer(WIDTH, HEIGHT, START, END)

Locations = Locations.Locations


def start(graphics):
    BFS.BFS.solve(GridContainer, graphics, START, END, WIDTH, HEIGHT)


def reset(graphics):
    GridContainer.init_grid()
    graphics.draw_grid(GridContainer.GRID)


def main():
    root = Tk()
    # gets rid of dashed line menu
    root.option_add('*tearOff', FALSE)

    root.title('Path finder')
    frame = ttk.Frame(root, width=WIDTH*SCALE, height=HEIGHT*SCALE)
    # This sets the windowID for pygame to use our window
    os.environ['SDL_WINDOWID'] = str(frame.winfo_id())
    graphics = Graphics.Graphics(WIDTH, HEIGHT, SCALE)
    # create the top menu bar
    menubar = Menu(root)
    root['menu'] = menubar
    menubar.add_command(label='Start',
                        command=lambda: start(graphics))
    menubar.add_command(label='Reset',
                        command=lambda: reset(graphics))
    alg_menu = Menu(menubar)
    alg = IntVar(0)
    alg_menu.add_radiobutton(label='BFS', variable='alg', value='0')
    alg_menu.add_radiobutton(label='A*', variable='alg', value='1')
    menubar.add_cascade(label="Alg", menu=alg_menu)

    # will not display without being packed
    frame.pack()

    GridContainer.init_grid()
    graphics.draw_grid(GridContainer.GRID)
    # graphics.draw_grid(GRID)
    root.protocol("WM_DELETE_WINDOW", lambda: destroy(root))
    while RUNNING:
        # Event Loop
        for event in pygame.event.get():
            e_type = event.type
            if e_type == pygame.MOUSEBUTTONDOWN or e_type == pygame.MOUSEBUTTONUP or e_type == pygame.MOUSEMOTION:
                x, y = event.pos
                pressed = None
                if e_type == pygame.MOUSEMOTION:
                    pressed = event.buttons[0]
                elif e_type == pygame.MOUSEBUTTONUP:
                    pressed = 0 if event.button == 1 else None
                elif e_type == pygame.MOUSEBUTTONDOWN:
                    pressed = 1 if event.button == 1 else None

                if pressed:
                    update_box(x // SCALE, y // SCALE, Locations.WALL, graphics, GridContainer)

        # Since WM_DESTROY_WINDOW is called async it could lead to an error without the check
        if RUNNING:
            root.update()


def destroy(root):
    global RUNNING
    RUNNING = False
    root.destroy()


main()
