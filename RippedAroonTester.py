# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 11:05:53 2017

@author: AmatVictoriaCuramIII
"""
from pandas_datareader import data
import pandas as pd
import numpy as np
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2016', end='01/01/2050') 
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Ranger'] = range(len(s))
k = pd.DataFrame(index = s['Ranger'])
AroonUp = []
AroonDown = []
AroonDate = []
tf = 7
AdjClose = s['Adj Close'].tolist()
AdjCloseSeries = pd.Series(AdjClose)
k['Adj Close'] = AdjCloseSeries
Date = s['Ranger'].tolist()
counter = tf
while counter < len(s):
    Aroon_Up = ((k['Adj Close'][counter-tf:counter].tolist().index(max
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
    Aroon_Down = ((k['Adj Close'][counter-tf:counter].tolist().index(min
            (k['Adj Close'][counter-tf:counter])))/float(tf)*100)
    AroonUp.append(Aroon_Up)
    AroonDown.append(Aroon_Down)
    AroonDate.append(Date[counter])
    counter = counter + 1
s = s[tf:]
AroonUpSeries = pd.Series(AroonUp, index=s.index)
AroonDownSeries = pd.Series(AroonDown, index=s.index)
s['AroonUp'] = AroonUpSeries
s['AroonDown'] = AroonDownSeries
s['Divergence'] = s['AroonUp'] - s['AroonDown']
s['Touch'] = np.where(s['Divergence'] < 86.065983, 1, 0) #long signal
s['Touch'] = np.where(s['Divergence'] > 92.797133, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                            s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1, 
                        s['Sustain'])
s['Sustain'] = np.where(s['Divergence'] > -22.227923, 0, s['Sustain']) 
s['Sustain'] = np.where(s['Divergence'] < 41.853571, 0, s['Sustain']) 
s['Regime'] = s['Touch'] + s['Sustain']
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))