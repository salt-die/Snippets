"""
Game of life, but newly born cells are the average color of their parents.

Press "r" to reset the universe, click to draw.
"""

import numpy as np
import scipy.ndimage as nd
import pygame

KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)

DIM = 500, 500
#DEAD_COLOR = (25, 31, 53)

universe = np.random.randint(2, size=DIM, dtype=np.uint8)
RGB = [np.random.randint(0, 256, size=DIM) for _ in range(3)]
RGB = [np.where(universe == 1, color, 0) for color in RGB]

pygame.init()
window = pygame.display.set_mode(DIM)
MOUSEDOWN = False
running = True

while running:

    for event in pygame.event.get():
        if event.type == 12: #Quit
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                universe = np.random.randint(2, size=DIM, dtype=np.uint8)
                RGB = [np.random.randint(0, 256, size=DIM) for _ in range(3)]
                RGB = [np.where(universe == 1, color, 0) for color in RGB]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                MOUSEDOWN = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                MOUSEDOWN = False

    if MOUSEDOWN:
        row, column = pygame.mouse.get_pos()
        universe[row-2:row+3, column-2:column+3] = 1
        for color in RGB:
            color[row-2:row+3, column-2:column+3] = np.random.randint(0, 256)

    neighbor_count = nd.convolve(universe, KERNEL, mode="constant")

    still_alive = np.where((universe == 1) & (neighbor_count > 1) & (neighbor_count < 4), 1, 0)
    new_borns = np.where((universe == 0) & (neighbor_count == 3), 1, 0)


    old_colors = [np.where(still_alive == 1, color, 0) for color in RGB]
    new_colors = [np.where(new_borns == 1, nd.convolve(color, KERNEL, mode="constant") / 3, 0) for color in RGB]

    universe = still_alive + new_borns
    RGB = [old_color + new_color for old_color, new_color in zip(old_colors, new_colors)]

    # pygame.surfarray.blit_array(window, np.dstack([np.where(color==0, dead, color)
    #                                                for dead, color in zip(DEAD_COLOR, RGB)]))

    pygame.surfarray.blit_array(window, np.dstack(RGB))
    pygame.display.update()

pygame.quit()
