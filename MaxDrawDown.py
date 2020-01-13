# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 22:37:50 2017

@author: AmatVictoriaCuramIII
"""

#This is a max drawdown calculator that was copied from unknown source.

import numpy as np
from numpy.lib.stride_tricks import as_strided
import pandas as pd
from WindowedView import WindowedView

def MaxDrawDown(x, window_size, min_periods=1):
    """Compute the rolling maximum drawdown of `x`.

    `x` must be a 1d numpy array.
    `min_periods` should satisfy `1 <= min_periods <= window_size`.

    Returns an 1d array with length `len(x) - min_periods + 1`.
    """
    if min_periods < window_size:
        pad = np.empty(window_size - min_periods)
        pad.fill(x[0])
        x = np.concatenate((pad, x))
    y = WindowedView(x, window_size)
    running_max_y = np.maximum.accumulate(y, axis=1)
    dd = y - running_max_y
    return dd.min(axis=1)
