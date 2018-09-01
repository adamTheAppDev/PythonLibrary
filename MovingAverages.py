# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:49:17 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
from pandas_datareader import data
def MovingAverages(s):
    s = data.DataReader(s, 'yahoo', start='1/1/1900', end='01/01/2050')
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1))
    s['42d'] = s['Adj Close'].rolling(window=56, center=False).mean()
    s['252d'] = s['Adj Close'].rolling(window=151, center=False).mean()
    s['42-252'] = s['42d'] - s['252d']
    s['Trend']= s['42-252']/s['Adj Close']
    s['Touch'] = np.where(s['42-252'] > .039073, 1, 0)
    s['Touch'] = np.where(s['42-252'] < -.031195, -1, s['Touch'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0)
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                         s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] > .051427, 0, s['Sustain'])
    s['Sustain'] = np.where(s['42-252'] < -.064538 , 0, s['Sustain'])
    s['Regime'] = s['Touch'] + s['Sustain']
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                    figsize=(8, 5))
    s[['42d', '252d', 'Close']].plot(grid=True, figsize=(8, 5))
    return s['Strategy']