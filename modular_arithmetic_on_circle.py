"""
Pygame implementation of https://www.youtube.com/watch?v=qhbuKbxJsk8

Use up/down to change number of points and left/right to change the multiplication factor
"""
from collections import defaultdict
import numpy as np
import pygame
from pygame.draw import aaline, circle

NUMBER_OF_POINTS = 40
FACTOR = 10
DIM = 500
FORECOLOR = (193, 169, 13)
BACKCOLOR = (37, 147, 206)

DIM_ARRAY = np.array([DIM, DIM])
CENTER = DIM_ARRAY // 2
RADIUS = DIM / 2 - 5

keys = defaultdict(bool)

pygame.init()

window = pygame.display.set_mode(DIM_ARRAY)
font = pygame.font.Font(pygame.font.get_default_font(), 20)
running = True

def update():
    def coordinates(point):
        theta = point * 2 * np.pi / NUMBER_OF_POINTS
        return RADIUS * np.array([np.sin(theta), np.cos(theta)]) + CENTER

    window.fill(BACKCOLOR)

    for point in range(NUMBER_OF_POINTS):
        start = coordinates(point)
        circle(window, FORECOLOR, start.astype(int), 4, 4)
        aaline(window, FORECOLOR, start, coordinates(FACTOR * point), 1)

    text_surfaces = [font.render(text, True, FORECOLOR)
                     for text in [f'Points: {NUMBER_OF_POINTS}', f'Factor: {round(FACTOR, 1)}']]

    window.blit(text_surfaces[0], dest=(10,0))
    window.blit(text_surfaces[1], dest=(10,20))
    pygame.display.update()

while running:
    update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    if keys[pygame.K_UP]:
        NUMBER_OF_POINTS += 1
    if keys[pygame.K_DOWN]:
        NUMBER_OF_POINTS -= 1 if NUMBER_OF_POINTS else 0
    if keys[pygame.K_LEFT]:
        FACTOR -= .1
    if keys[pygame.K_RIGHT]:
        FACTOR += .1

pygame.quit()
