# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a single issue strategy 

#Import modules
import numpy as np
from pandas_datareader import data
import pandas as pd

#Variable assignment
ticker = '^GSPC'
window = 20

#Request data
s = YahooGrabber(ticker)

#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)

#Money flow multiplier calculation
s['MFMultiplier'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#MF time volume (non-normalized volume..)
s['MFVolume'] = (s['Volume'] * s['MFMultiplier'])

#Horizontal baseline
s['ZeroLine'] = 0

#Chaikin money flow calculation
s['CMF'] = s['MFVolume'].rolling(center=False, window=window).sum(
        )/s['Volume'].rolling(center=False, window=window).sum()

#Indicator graph
s[['CMF','ZeroLine']][window:].plot(grid=True, figsize=(8,3))

#Trading strategy
s['Touch'] = np.where(s['CMF'] < 0, 1,0) #long signal
s['Touch'] = np.where(s['CMF'] > 0, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                 s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
s['Sustain'] = np.where(s['CMF'] > 0.4, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['CMF'] < -0.4, 0, s['Sustain']) #never actually true when optimized

#Position directions
s['Regime'] = s['Touch'] + s['Sustain']

#Apply positions to log returns
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)

#Performance metrics
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()

#Graph strategy vs returns
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
#Performance metric
print(sharpe)
