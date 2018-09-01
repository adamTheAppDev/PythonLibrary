# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:52:49 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
import pandas as pd
from pandas_datareader import data
s1 = data.DataReader('^GSPC', 'yahoo', start='01/01/1950', end='01/01/1972')
testset1 = pd.read_pickle('SP500RSI50_72_4M')
testset1 = testset1.loc[:,~testset1.columns.duplicated()]
for i in testset1:
    a = testset1[i].iloc[0]
    aa = a.astype(int)
    b = testset1[i].iloc[1]
    c = testset1[i].iloc[2]
    d = testset1[i].iloc[3]
    e = testset1[i].iloc[4]
    openspace = []
    openseries = pd.Series()
    s1['LogRet'] = np.log(s1['Adj Close']/s1['Adj Close'].shift(1)) 
    s1['LogRet'] = s1['LogRet'].fillna(0)
    close = s1['Adj Close']
    window = aa
    delta = close.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    AvgGain = up.rolling(window).mean()
    AvgLoss = down.abs().rolling(window).mean() 
    RS = AvgGain/AvgLoss
    RSI = 100 - (100/(1.0+RS))
    s1['RSI'] = RSI
    s1['RSI'] = s1['RSI'].fillna(0)
    s1['Touch'] = np.where(s1['RSI'] < b, 1, 0) #long signal
    s1['Touch'] = np.where(s1['RSI'] > c, -1, s1['Touch']) #short signal
    s1['Sustain'] = np.where(s1['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s1['Sustain'] = np.where(s1['Sustain'].shift(1) == 1, 1, 
                                  s1['Sustain']) 
    s1['Sustain'] = np.where(s1['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s1['Sustain'] = np.where(s1['Sustain'].shift(1) == -1, -1,
                                   s1['Sustain']) 
    s1['Sustain'] = np.where(s1['RSI'] > d, 0, s1['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s1['Sustain'] = np.where(s1['RSI'] < e, 0, s1['Sustain']) #never actually true when optimized
    s1['Regime'] = s1['Touch'] + s1['Sustain']
    s1['Strategy'] = (s1['Regime'][window:]).shift(1)*s1['LogRet'][window:]
    s1['Strategy'] = s1['Strategy'].fillna(0)
    endgains = 1
    endreturns = 1
    var = []
    avar = []
    intvar = []
    for g in s1['LogRet']:
        slate = endreturns * (1+g)
        endreturns = slate
    for q in s1['Strategy']:
        otherslate = endgains * (1+q)
        endgains = otherslate
#    if endreturns > endgains:
#        continue       
    sharpe = (s1['Strategy'].mean()-s1['LogRet'].mean())/s1['Strategy'].std()






