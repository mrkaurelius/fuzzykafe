#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:42:41 2020

@author: mrk

source https://github.com/scikit-fuzzy/scikit-fuzzy

"""

import numpy as np


def trimf(x, abc):
    """
    Triangular membership function generator.
    Parameters
    ----------
    x : 1d array
        Independent variable.
    abc : 1d array, length 3
        Three-element vector controlling shape of triangular function.
        Requires a <= b <= c.
    Returns
    -------
    y : 1d array
        Triangular membership function.
    """
    assert len(abc) == 3, 'abc parameter must have exactly three elements.'
    a, b, c = np.r_[abc]     # Zero-indexing in Python
    assert a <= b and b <= c, 'abc requires the three elements a <= b <= c.'

    y = np.zeros(len(x))

    # Left side
    if a != b:
        idx = np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = (x[idx] - a) / float(b - a)

    # Right side
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))[0]
        y[idx] = (c - x[idx]) / float(c - b)

    idx = np.nonzero(x == b)
    y[idx] = 1
    return y

#%% interp membership

def interp_membership(x, xmf, xx, zero_outside_x=True):
    """
    Find the degree of membership ``u(xx)`` for a given value of ``x = xx``.
    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for ``x``.  Same length as ``x``.
    xx : float or array of floats
        Value(s) on universe ``x`` where the interpolated membership is
        desired.
    zero_outside_x : bool, optional
        Defines the behavior if ``xx`` contains value(s) which are outside the
        universe range as defined by ``x``.  If `True` (default), all
        extrapolated values will be zero.  If `False`, the first or last value
        in ``x`` will be what is returned to the left or right of the range,
        respectively.
    Returns
    -------
    xxmf : float or array of floats
        Membership function value at ``xx``, ``u(xx)``.  If ``xx`` is a single
        value, this will be a single value; if it is an array or iterable the
        result will be returned as a NumPy array of like shape.
    Notes
    -----
    For use in Fuzzy Logic, where an interpolated discrete membership function
    u(x) for discrete values of x on the universe of ``x`` is given. Then,
    consider a new value x = xx, which does not correspond to any discrete
    values of ``x``. This function computes the membership value ``u(xx)``
    corresponding to the value ``xx`` using linear interpolation.
    """
    # Not much beats NumPy's built-in interpolation
    if not zero_outside_x:
        kwargs = (None, None)
    else:
        kwargs = (0.0, 0.0)
    return np.interp(xx, x, xmf, left=kwargs[0], right=kwargs[1])

#%% defuzz centroid

'''
defuzz.py
'''

def centroid(x, mfx):
    """
    Defuzzification using centroid (`center of gravity`) method.
    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function
    Returns
    -------
    u : 1d array, length M
        Defuzzified result
    See also
    --------
    skfuzzy.defuzzify.defuzz, skfuzzy.defuzzify.dcentroid
    """

    '''
    As we suppose linearity between each pair of points of x, we can calculate
    the exact area of the figure (a triangle or a rectangle).
    '''

    sum_moment_area = 0.0
    sum_area = 0.0

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return (x[0] * mfx[0]
                / np.fmax(mfx[0], np.finfo(float).eps).astype(float))

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not (y1 == y2 == 0.0 or x1 == x2):
            if y1 == y2:  # rectangle
                moment = 0.5 * (x1 + x2)
                area = (x2 - x1) * y1
            elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
                moment = 2.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
                moment = 1.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y1
            else:
                moment = ((2.0 / 3.0 * (x2 - x1) * (y2 + 0.5 * y1))
                          / (y1 + y2) + x1)
                area = 0.5 * (x2 - x1) * (y1 + y2)

            sum_moment_area += moment * area
            sum_area += area

    return (sum_moment_area
            / np.fmax(sum_area, np.finfo(float).eps).astype(float))
