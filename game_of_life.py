"""
Conway's Game of Life calculated with convolutions and displayed in terminal.
"""

import os
import time
import numpy as np
import scipy.ndimage as nd

# This kernel counts the live neighbors
KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)

COLUMNS, ROWS = os.get_terminal_size()
DIM = ROWS, COLUMNS

universe = np.random.randint(2, size=DIM, dtype=np.uint8)

# We initialize these arrays so we can perform all operations in place.
convolved_universe = np.zeros_like(universe)
intermediate_1 = np.zeros_like(universe)
intermediate_2 = np.zeros_like(universe)
intermediate_3 = np.zeros_like(universe)

while True:
    for _ in range(1000):
        os.system("clear || cls")  # Clears the terminal
        print(*("".join("M" if cell else " " for cell in row) for row in universe), sep="\n")
        nd.convolve(universe, KERNEL, mode="constant", output=convolved_universe)
        # It isn't pretty, but doing the following logic in place:
        # universe = (((universe == 1) & (convolved_universe > 1) & (convolved_universe < 4)) |
        #           ((universe == 0) & (convolved_universe == 3))).astype(np.uint8)
        np.equal(universe, 1, out=intermediate_1)
        np.greater(convolved_universe, 1, out=intermediate_2)
        np.logical_and(intermediate_1, intermediate_2, out=intermediate_1)
        np.less(convolved_universe, 4, out=intermediate_2)
        np.logical_and(intermediate_1, intermediate_2, out=intermediate_1)
        np.equal(universe, 0, out=intermediate_2)
        np.equal(convolved_universe, 3, out=intermediate_3)
        np.logical_and(intermediate_2, intermediate_3, out=intermediate_2)
        np.logical_or(intermediate_1, intermediate_2, out=universe)
        time.sleep(.1)
    universe = np.random.randint(2, size=DIM, dtype=np.uint8)
