# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:28:23 2017

@author: AmatVictoriaCuramIII
"""

#pandas_datareader is deprecated, use YahooGrabber
#This is a summary statistic calculator

import numpy as np
from pandas_datareader import data
def CoeffVar(s):
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.mean(s['LogRet'])*252
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    s['CoeffVar'] = s['SD']/s['Mean']
    return s['CoeffVar'].tail(1)
