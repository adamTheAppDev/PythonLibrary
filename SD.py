# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:05:58 2017

@author: AmatVictoriaCuramIII
"""

#This is a summary statistic + database query tool

import numpy as np
from pandas_datareader import data
def SD(s):
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    return s['SD'].tail(1)
