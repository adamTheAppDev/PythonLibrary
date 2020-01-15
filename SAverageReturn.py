# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:05:05 2017

@author: AmatVictoriaCuramIII
"""

#This is a summary statistic + database query tool

import numpy as np
def SAverageReturn(s):
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.mean(s['LogRet'])*252
    return s['Mean'].tail(1)
