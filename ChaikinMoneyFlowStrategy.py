# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 14:31:49 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
from pandas_datareader import data
import pandas as pd
ticker = '^GSPC'
window = 20
s = data.DataReader(ticker, 'yahoo', start='01/01/2000', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['MFMultiplier'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['MFVolume'] = (s['Volume'] * s['MFMultiplier'])
s['ZeroLine'] = 0
s['CMF'] = s['MFVolume'].rolling(center=False, window=window).sum(
        )/s['Volume'].rolling(center=False, window=window).sum()
s[['CMF','ZeroLine']][window:].plot(grid=True, figsize=(8,3))
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
s['Regime'] = s['Touch'] + s['Sustain']
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))
Length = len(s['LogRet'])
Range = range(0,Length)
print(sharpe)
