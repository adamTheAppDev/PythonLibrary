# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:00:21 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
def SRelStrInd(s):
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    close = s['Adj Close']
    window = 14  
    delta = close.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    AvgGain = up.rolling(window).mean()
    AvgLoss = down.abs().rolling(window).mean() 
    RS = AvgGain/AvgLoss
    RSI = 100 - (100/(1.0+RS))
    return RSI.tail(1)

