import numpy as np
from PIL import Image

LEFT, RIGHT = -2.0, 1.0
BOTTOM, TOP = -1.5, 1.5
WIDTH, HEIGHT = 512, 512

ITERATIONS = 256

xs = np.linspace(LEFT, RIGHT, WIDTH)
ys = np.linspace(TOP, BOTTOM, HEIGHT)
xs, ys = np.meshgrid(xs, ys)
C = xs + ys * 1j

Z = np.zeros_like(C)
escapes = np.zeros(C.shape, dtype=np.uint16)

for i in range(1, ITERATIONS):
    Z = np.where(escapes, 0, Z**2 + C)
    escapes[np.abs(Z) > 2] = i


#Coloring
escapes %= 16
R = [66, 25, 9, 4, 0, 12, 24, 57, 134, 211, 241, 248, 255, 204, 153, 106]
G = [30, 7, 1, 4, 7, 44, 82, 125, 181, 236, 233, 201, 170, 128, 87, 52]
B = [15, 26, 47, 73, 100, 138, 177, 209, 229, 248, 191, 95, 0, 0, 0, 3]

RGB = [np.where(escapes, arr[escapes], 0) for arr in map(np.array, (R, G, B))]
image = Image.fromarray(np.dstack(RGB).astype(np.uint8))
image.show()
