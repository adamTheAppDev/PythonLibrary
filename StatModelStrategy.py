# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 23:28:42 2018

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester for a z-score based model

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

Ticker1 = 'UVXY'

Asset1 = YahooGrabber(Ticker1)
Rollwindow = 5
Zscorethreshold = 3
hold = 10
ranger = range(0, hold)
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['LogRet+1'] = Asset1['LogRet'] + 1
meanreturn = Asset1['LogRet'].mean()
stdreturn = Asset1['LogRet'].std()
Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
rollmeanreturn = Asset1['RollingRet'].mean()
rollstdreturn = Asset1['RollingRet'].std()
Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn
Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                -1, 0)
for r in ranger:
    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
Asset1['OriginalTrade'] = 0
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1 
Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet']
Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
