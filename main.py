'''The start of the program'''
from path.world import World

SCALE = 10
WIDTH = 50
HEIGHT = 50


def main():
    '''The main loop for the program'''
    world = World(WIDTH, HEIGHT, SCALE)
    while True:
        if not world.handle_events():
            break
        world.update()
        world.draw()


main()
