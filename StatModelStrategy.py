# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester for a z-score based model

#Import modules
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber

#Assign ticker
Ticker1 = 'UVXY'

#Request data
Asset1 = YahooGrabber(Ticker1)

#Variable assignment
Rollwindow = 5
Zscorethreshold = 3
hold = 10
ranger = range(0, hold)

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['LogRet+1'] = Asset1['LogRet'] + 1
#Summary statistics
meanreturn = Asset1['LogRet'].mean()
stdreturn = Asset1['LogRet'].std()
#Calculate z-score
Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
#Rolling returns
Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
#Summary statistics
rollmeanreturn = Asset1['RollingRet'].mean()
rollstdreturn = Asset1['RollingRet'].std()
#Calculate rolling z-score
Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn
#Directional methodology
Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                -1, 0)
#Forward fill position for holding period
for r in ranger:
    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
#Zeros    
Asset1['OriginalTrade'] = 0
#Initital signal in stream of -1s
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1 
#Apply position to returns
Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet']
#Grahpical display
Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
