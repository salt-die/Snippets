import numpy as np
import pygame

#Modify these as you will
DIM = 800
FORECOLOR = 193, 169, 13
BACKCOLOR = 17, 107, 156
pendulums = [DIM/64 * i for i in range(11, 32)]
START_ANGLE = np.pi/3
TIME_DELTA = np.pi / 100

#But Leave these alone
DIM_ARRAY = np.array([DIM, DIM])
CENTER = DIM_ARRAY / 2
BLACK = 0, 0, 0

pygame.init()

window = pygame.display.set_mode(DIM_ARRAY)

def coordinates(time, radius):
    theta = START_ANGLE * np.cos((9.8/ radius)**.5 * time)
    return radius * np.array([np.sin(theta), np.cos(theta)]) + CENTER

time = 0
running = True
while running:

    window.fill(BACKCOLOR)
    for pendulum in pendulums:
        pygame.draw.aaline(window, FORECOLOR, coordinates(time, pendulum), CENTER, 1)
    #Separate loop so lines don't draw on top of circles
    for pendulum in pendulums:
        pygame.draw.circle(window, BLACK, coordinates(time, pendulum).astype(int), 10, 10)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time += TIME_DELTA

pygame.quit()
