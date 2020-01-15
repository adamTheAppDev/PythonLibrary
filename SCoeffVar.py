# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:28:23 2017

@author: AmatVictoriaCuramIII
"""

#This is a summary statistic + database query tool

import numpy as np
def SCoeffVar(s):
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['Mean'] = np.mean(s['LogRet'])*252
    s['SD'] = np.std(s['LogRet'])*np.sqrt(252)
    s['CoeffVar'] = s['SD']/s['Mean']
    return s['CoeffVar'].tail(1)
