#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


import numpy as np
import scipy.spatial.distance


def l2_normalize(fX):

    norm = np.sqrt(np.sum(fX ** 2, axis=1))
    norm[norm == 0] = 1.
    return (fX.T / norm).T


def get_range(metric='euclidean'):
    return {
        'angular': (0, np.pi),
        'euclidean': (0, 2),
        'sqeuclidean': (0, 4),
        'cosine': (-1.0, 1.0)
    }.get(metric, None)


def pdist(fX, metric='euclidean', **kwargs):

    if metric == 'angular':
        cosine = scipy.spatial.distance.pdist(
            fX, metric='cosine', **kwargs)
        return np.arccos(np.clip(1.0 - cosine, -1.0, 1.0))

    return scipy.spatial.distance.pdist(fX, metric=metric, **kwargs)


def cdist(fX_trn, fX_tst, metric='euclidean', **kwargs):

    if metric == 'angular':
        cosine = scipy.spatial.distance.cdist(
            fX_trn, fX_tst, metric='cosine', **kwargs)
        return np.arccos(np.clip(1.0 - cosine, -1.0, 1.0))

    return scipy.spatial.distance.cdist(
        fX_trn, fX_tst, metric=metric, **kwargs)
def to_condensed(i, j):
    """Compute index in condensed pdist matrix

           0 1 2 3 4
        0  . . . . .
        1  0 . . . .  --> 0 1 2 3 4 5 6 7 8 9
        2  1 2 . . .                      ^
      > 3  3 4 5 . .
        4  6 7 8 9 .
               ^
    Parameters
    ----------
    i, j : int
        Indices in squared pdist matrix

    Returns
    -------
    k : int
        Index in condensed pdist matrix
    """

    assert i != j, "no diagonal elements in condensed matrix"
    if i < j:
        i, j = j, i

    return j + int(.5 * (i * (i - 1)))
