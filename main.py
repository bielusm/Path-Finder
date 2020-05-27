'''The start of the program'''
import pygame
from path.world import World


WIDTH = 50
HEIGHT = 50


def main():
    '''The main loop for the program'''
    world = World(WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick()/1000.0
        if not world.handle_events():
            break
        world.update(time_delta)
        world.draw()


main()
