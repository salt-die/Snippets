import numpy as np
import pygame

#Modify these as you will
DIM = 800
FORECOLOR = 193, 169, 13
BACKCOLOR = 17, 107, 156
MAX_RADIUS = 60
NUMBER_OF_PENDULUMS = 20
pendulums = [MAX_RADIUS - n for n in range(NUMBER_OF_PENDULUMS)]
START_ANGLE = np.pi / 4
TIME_DELTA = np.pi / 200

#But Leave these alone
DIM_ARRAY = np.array([DIM, DIM])
CENTER = DIM_ARRAY / 2
BLACK = 0, 0, 0

pygame.init()

window = pygame.display.set_mode(DIM_ARRAY)

def coordinates(time, radius):
    theta = START_ANGLE * np.cos((9.8 / radius)**.5 * time)
    return DIM/(2 * MAX_RADIUS) * radius * np.array([np.sin(theta), np.cos(theta)]) + CENTER

time = 0
running = True
while running:

    window.fill(BACKCOLOR)
    for pendulum in pendulums:
        pygame.draw.aaline(window, FORECOLOR, coordinates(time, pendulum), CENTER, 1)
    #Separate loop so lines don't draw on top of circles
    for pendulum in pendulums:
        # for i in range(1,5):
        #     trans = pygame.Surface((15,15))
        #     trans.fill(BACKCOLOR)
        #     trans.set_alpha(255/4 * i)
        #     pygame.draw.circle(trans, BLACK, (7,7), 10, 10)
        #     window.blit(trans, coordinates(time - (4 - i), pendulum).astype(int))
        pygame.draw.circle(window, BLACK, coordinates(time, pendulum).astype(int), 10, 10)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time += TIME_DELTA

pygame.quit()
