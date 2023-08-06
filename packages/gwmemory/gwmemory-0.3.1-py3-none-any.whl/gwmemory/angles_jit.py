#!/usr/bin/python3
from functools import partial

import numpy as np
from numba import jit
from scipy.integrate import nquad

from . import harmonics_jit


@jit
def _omega_jit(omega_ij, inc, phase):

    # wx, wy = wave_frame(inc, phase)
    cth, sth = np.cos(inc), np.sin(inc)
    cph, sph = np.cos(phase), np.sin(phase)
    cps, sps = np.cos(phase), np.sin(phase)

    u = np.array([cph * cth, cth * sph, -sth])
    v = np.array([-sph, cph, 0])

    wx = -u * sps - v * cps
    wy = -u * cps + v * sps

    e_plus = np.outer(wx, wx) - np.outer(wy, wy)
    e_cross = np.outer(wx, wy) + np.outer(wy, wx)
    omega_plus = np.trace(omega_ij @ e_plus)
    omega_cross = np.trace(omega_ij @ e_cross)
    return omega_plus, omega_cross


@jit
def integrand(cos_inc, cos_theta, phi, lm1, lm2, ell):
    inc = np.arccos(cos_inc)
    theta = np.arccos(cos_theta)
    ss = -2
    phase = 0
    l1, m1 = lm1
    l2, m2 = lm2

    y_lmlm_factor = (
        harmonics_jit.sYlm(ss, l1, m1, theta, phi)
        * np.conjugate(harmonics_jit.sYlm(ss, l2, m2, theta, phi))
        * (-1) ** (l1 + l2)
    )

    n = np.array([
        np.cos(phi) * np.sin(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(theta),
    ])
    line_of_sight = np.array([np.sin(inc) * np.cos(phase), np.sin(inc) * np.sin(phase), np.cos(inc)])
    n_dot_line_of_sight = n.dot(line_of_sight)
    lambda_mat = np.outer(n, n) / (1 - n_dot_line_of_sight)
    proj = np.identity(3) - np.outer(line_of_sight, line_of_sight)
    lambda_mat -= proj * np.trace(lambda_mat) / 2

    plus, cross = _omega_jit(lambda_mat, inc, phase)

    lambda_lmlm = (plus - 1j * cross) / 2 * y_lmlm_factor

    delta_m = m1 - m2
    return -np.real(2 * np.pi * lambda_lmlm * np.conjugate(harmonics_jit.sYlm(-2, ell, -delta_m, inc, phase)))


def numerical_gamma(lm1, lm2, ell, return_error=False):
    result = nquad(
        partial(integrand, lm1=lm1, lm2=lm2, ell=ell),
        [(-1, 1), (-1, 1), (0, 2 * np.pi)],
    )
    if return_error:
        return result
    else:
        return result[0]
