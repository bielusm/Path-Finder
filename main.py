'''The start of the program'''
from path.world import World

WIDTH = 50
HEIGHT = 50


def main():
    '''The start of the program'''
    world = World(WIDTH, HEIGHT)
    world.loop()

main()
