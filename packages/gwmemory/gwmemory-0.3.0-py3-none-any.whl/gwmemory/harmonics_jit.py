# ----------------------------------------------------------
#
# This module computes spin-weighted spherical harmonics.
#
# Released under the MIT License.
# (C) Christian Reisswig 2009-2011
# Modified Colm Talbot 2018
#
# ----------------------------------------------------------
import numpy as np
from numba import jit

FACTORIAL_TABLE = np.array([
    1, 1, 2, 6, 24, 120, 720, 5040, 40320,
    362880, 3628800, 39916800, 479001600,
    6227020800, 87178291200, 1307674368000,
    20922789888000, 355687428096000, 6402373705728000,
    121645100408832000, 2432902008176640000
], dtype='int64')


# coefficient function
@jit
def Cslm(s, l, m):
    return (
        l**2 * (4 * l**2 - 1)
        / ((l**2 - m**2) * (l**2 - s**2))
    ) ** 0.5


# recursion function
@jit
def s_lambda_lm(s, l, m, x):
    Pm = (-0.5) ** m
    Pm *= (1 + x) ** ((m - s) / 2) * (1 - x) ** ((m + s) / 2)
    Pm *= (
        FACTORIAL_TABLE[2 * m + 1] /
        (4 * np.pi * FACTORIAL_TABLE[m + s] * FACTORIAL_TABLE[m - s])
    )**0.5
    if l == m:
        return Pm
    Pm1 = (x + s * 1.0 / (m + 1)) * Cslm(s, m + 1, m) * Pm
    if l == m + 1:
        return Pm1
    else:
        for n in range(m + 2, l + 1):
            Pn = (
                (x + s * m * 1 / (n * (n - 1))) * Cslm(s, n, m) * Pm1
                - Cslm(s, n, m) / Cslm(s, n - 1, m) * Pm
            )
            Pm = Pm1
            Pm1 = Pn
        return Pn


@jit
def sYlm(ss, ll, mm, theta, phi):
    """Calculate spin-weighted harmonic"""
    Pm = 1.0
    l = ll
    m = mm
    s = ss
    if l < 0:
        return 0
    if abs(m) > l or l < abs(s):
        return 0
    if abs(mm) < abs(ss):
        s = mm
        m = ss
        if (m + s) % 2:
            Pm = -Pm
    if m < 0:
        s = -s
        m = -m
        if (m + s) % 2:
            Pm = -Pm
    result = Pm * s_lambda_lm(s, l, m, np.cos(theta))
    return result * np.exp(1j * mm * phi)


@jit
def lmax_modes(lmax):
    """Compute all (l, m) pairs with 2<=l<=lmax"""
    return [(l, m) for l in range(2, lmax + 1) for m in range(-l, l + 1)]
