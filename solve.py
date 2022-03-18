
from scipy.optimize import least_squares
import numpy as np

from separate import angles


class PosSolver:

    def __init__(self):
        self.dataset = None

    def collectError(self, p):
        if self.dataset is None:
            return

        err = 0
        x,y = self.dataset.imagedata.size
        x/=2
        y/=2
        for k in self.dataset.lines:
            err += abs(angles(p, 0, k.x1-x, -k.y1+y, k.x2-x, -y+k.y2, k.axis)) #inverted y because origin of image is upper left.

        return err

    def solve(self):
        p = np.array([100, 0, 0])
        res = least_squares(self.collectError, p)
        print(res)

        p = np.array([1, 0, 0])
        res = least_squares(self.collectError, p)
        print(res)

        return res
