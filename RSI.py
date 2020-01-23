# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:00:21 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester
#pandas_datareader is deprecated, use YahooGrabber

from pandas_datareader import data
import numpy as np
#def RelStrInd(s):
s = data.DataReader('^GSPC', 'yahoo', start='1/1/1950', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
close = s['Adj Close']
window = 26  
delta = close.diff()
delta = delta[1:]
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
AvgGain = up.rolling(window).mean()
AvgLoss = down.abs().rolling(window).mean() 
RS = AvgGain/AvgLoss
RSI = 100 - (100/(1.0+RS))
#    RSI.plot(grid=True, figsize=(8, 5))
    #return RSI.tail(1)
s['RSI'] = RSI
s['RSI'] = s['RSI'].fillna(0)
s['Touch'] = np.where(s['RSI'] < 80.094404, 1,0) #long signal
s['Touch'] = np.where(s['RSI'] > 82.281912, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                   s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
s['Sustain'] = np.where(s['RSI'] > 97.169695, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
s['Sustain'] = np.where(s['RSI'] < 82.356067, 0, s['Sustain']) #never actually true when optimized
s['Regime'] = s['Touch'] + s['Sustain']
s['Strategy'] = (s['Regime'][window:]).shift(1)*s['LogRet'][window:]
s['Strategy'] = s['Strategy'].fillna(0)
endgains = 1
endreturns = 1
for g in s['LogRet']:
    slate = endreturns * (1+g)
    endreturns = slate
for q in s['Strategy']:
    otherslate = endgains * (1+q)
    endgains = otherslate
sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
s[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                                figsize=(8,5))
print(endreturns)
print(endgains)                                                
print(sharpe)
