import pygame


def update_box(x, y, val, graphics, grid_container):
    grid_container.update_box(x, y, val)
    graphics.draw_box(x, y, val)
    pygame.display.flip()
