# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 22:41:25 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
from numpy.lib.stride_tricks import as_strided
import pandas as pd
#Stolen windowed view
def WindowedView(x, window_size):
    """Creat a 2d windowed view of a 1d array.

    `x` must be a 1d numpy array.

    `numpy.lib.stride_tricks.as_strided` is used to create the view.
    The data is not copied.

    Example:

    >>> x = np.array([1, 2, 3, 4, 5, 6])
    >>> windowed_view(x, 3)
    array([[1, 2, 3],
           [2, 3, 4],
           [3, 4, 5],
           [4, 5, 6]])
    """
    y = as_strided(x, shape=(x.size - window_size + 1, window_size),
                   strides=(x.strides[0], x.strides[0]))
    return y