'''The start of the program'''
from time import sleep
from path.world import World

SCALE = 10
WIDTH = 50
HEIGHT = 50


def main():
    '''The main loop for the program'''
    world = World(WIDTH, HEIGHT, SCALE)
    while True:
        sleep(0.005)
        if not world.handle_events():
            break
        world.update()
        world.draw()


main()
