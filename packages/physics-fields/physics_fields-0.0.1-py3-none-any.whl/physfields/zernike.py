import numpy as np
import collections
from typing import Optional


from .scalarfield import ScalarField
from .vectorfield import VectorField


def triangular_row(n: int) -> int:
    """ Return the 0-indexed row in which nth triangular number is found """
    assert(isinstance(n, int))
    return int(np.floor(np.sqrt(1 + 8 * n) - 1) / 2)


def triangular_less(n: int) -> int:
    """ Return the largest triangular number less than n """
    assert(isinstance(n, int))
    row = triangular_row(n)
    return row * (row + 1) // 2


def triangular_column(n: int) -> int:
    """ Return the column of number n in triangle """
    assert(isinstance(n, int))
    return n - triangular_less(n)


SR2 = np.sqrt(2)
SROH = 1 / np.sqrt(2)

class Zernike(ScalarField):
    """
        Lazily evaluated scalar Zernike polynomial
    """

    def __init__(self, n: int, l: int, masked: bool=True):
        """
            A new Zernike scalar field defined in terms of radial and angular component order n and l:
            n: int, non-negative radial component order
            l: int, angular component order, |l| < n and l = n (mod 2)
            masked: mask the area outside the unit disk with numpy.ma
        """
        if abs(l) > n or (l + n) % 2 != 0:
            raise NotImplementedError("|l| must be < n and also l = n (mod 2)")

        self.n = n
        self.l = l
        self.absl = abs(l)
        self.masked = masked

        # Set Noll and ANSI indices for convenience
        self.noll = n * (n + 1) // 2 + abs(l) + (1 if (l >= 0 and n % 4 in [2, 3]) or (l <= 0 and n % 4 in [0, 1]) else 0)
        self.ansi = (n * (n + 2) + l) / 2

    @staticmethod
    def noll_to_nl(noll: int) -> tuple[int, int]:
        n = triangular_row(noll - 1)
        l = (-1)**noll * ((n % 2) + 2 * int((triangular_column(noll - 1) + ((n + 1) % 2)) / 2))
        return n, l

    @staticmethod
    def ansi_to_nl(ansi: int) -> tuple[int, int]:
        n = triangular_row(ansi)
        l = (ansi - triangular_less(ansi)) * 2 - n
        return n, l

    @classmethod
    def from_noll(cls, noll: int) -> 'Zernike':
        """ Static constructor from Noll index """
        return cls(*cls.noll_to_nl(noll))

    @classmethod
    def from_ANSI(cls, ansi: int) -> 'Zernike':
        """ Static constructor from ANSI index """
        return cls(*cls.ansi_to_nl(ansi))

    def radial_part(self, x, y):
        r = np.sqrt(x * x + y * y)
        return sum([
            (-1)**s * np.math.factorial(self.n - s) /
            (np.math.factorial(s) * np.math.factorial((self.n + self.absl) // 2 - s) * np.math.factorial((self.n - self.absl) // 2 - s))
            * r ** (self.n - 2 * s)
            for s in range(0, (self.n - self.absl) // 2 + 1)],
        )

    def angular_part(self, x, y):
        if self.l == 0:
            return 1
        else:
            fun = np.cos if self.l > 0 else np.sin
            return np.sqrt(2) * fun(self.absl * np.arctan2(y, x))

    def function(self, x, y):
        z = np.sqrt(self.n + 1) * self.radial_part(x, y) * self.angular_part(x, y)
        if self.masked:
            return np.ma.masked_where(x * x + y * y > 1, z)
        else:
            return z


class ZernikeVector(VectorField):
    """
        Lazily evaluated vector Zernike polynomial (Zhao & Burge, 2007, 2008)
    """
    def __init__(self, n: int, l: int, rotational: Optional[bool]=None, masked: bool=True):
        if abs(l) > n or (l + n) % 2 != 0:
            raise NotImplementedError("|l| must be <= n and also l = n (mod 2)")
        if abs(l) == n and rotational is not None:
            raise NotImplementedError("Polynomials with |l| = n are always Laplacian")
        if abs(l) != n and rotational is None:
            raise NotImplementedError("Polynomials with |l| != n have to be rotational or diverging")

        self.n = n
        self.l = l
        self.r = rotational

        if n == 0:
            super().__init__(ScalarField(), ScalarField())
        elif n == 1:
            if l == -1:
                super().__init__(Zernike(0, 0), ScalarField())
            else:
                super().__init__(ScalarField(), Zernike(0, 0))
        else:
            m = n - 1
            rot = -1 if rotational else 1

            if n == -l:
                super().__init__(SROH * Zernike(m, -m), SROH * Zernike(m, m))
            elif n == l:
                super().__init__(SROH * Zernike(m, m), -SROH * Zernike(m, -m))
            elif l == 0:
                super().__init__(SROH * Zernike(m, rot), SROH * rot * Zernike(m, -rot))
            elif abs(l) == 1:
                if l == -1:
                    super().__init__(0.5 * Zernike(m, -2), 0.5 * ((rot * SR2) * Zernike(m, 0) - Zernike(m, 2)))
                else:
                    super().__init__(0.5 * (SR2 * Zernike(m, 0) + rot * Zernike(m, 2)), (0.5 * rot) * Zernike(m, -2))
            else:
                super().__init__(0.5 * (Zernike(m, l - 1) + rot * Zernike(m, l + 1)), 0.5 * (rot * Zernike(m, -l - 1) - Zernike(m, -l + 1)))
