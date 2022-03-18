from collections import namedtuple

import numpy as np
from PIL import Image


line = namedtuple('Line', ['x1', 'y1', 'x2', 'y2', 'axis', 'canvas_id'])
right = np.array([1, 0, 0])
forward = np.array([0, 1, 0])
up = np.array([0, 0, 1])


class Dataset:

    def __init__(self, imgFile):
        self.lines = []
        self.imagedata = Image.open(imgFile)


def magnitude(x):
    return np.sqrt(x.dot(x))


def angles(p, alpha, kx1, ky1, kx2, ky2, axis):

    r = np.cross(p, up)  # @Todo introduce angle here, rotate "up" along "p" first.
    q = np.cross(p, r)
    r = np.cross(p, q)

    r /= magnitude(r)
    q /= magnitude(q)

    p1 = kx1 * r + ky1 * q + p
    p2 = kx2 * r + ky2 * q + p
    p3 = 2 * p1 + 2 * p

    d1 = (p2 - p1) / (magnitude(p2 - p1))
    d2 = (p3 - p1) / (magnitude(p3 - p1))

    n = np.cross(d1, d2)
    n /= magnitude(n)

    return abs(n[axis])
