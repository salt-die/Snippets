"""
Dragon curve generated with numpy.

Original was found here:
https://github.com/Brenn10/programming_exercises/blob/master/fun/dragoncurve.py

But we've vectorized as much as possible with einsums.
"""

import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 10
curve = np.array([[0., 1.], [0., 0.], [1., 0.]])
rotate45_scale_by_half = np.array([[.5, -.5], [.5, .5]])
move = np.array([0., 1.])
rotate45 = np.array([[0., -1.], [1., 0.]])

for i in range(ITERATIONS):
    np.subtract(curve, move, out=curve)
    # Element-wise dot product --- curve is scaled and rotated
    np.einsum('ik,kj->ij', curve, rotate45_scale_by_half, out=curve)
    np.add(curve, move, out=curve)
    # 2nd half of the curve is rotated a further 45 degrees
    curve_2 = np.einsum('ik,kj->ij', curve[-2::-1], rotate45)
    curve = np.concatenate([curve, curve_2])

plt.plot(*curve.T)
plt.axis('off')
plt.show()