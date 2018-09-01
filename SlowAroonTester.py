# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 10:18:54 2017

@author: AmatVictoriaCuramIII
"""
from pandas_datareader import data
import pandas as pd
import numpy as np
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='01/01/2013', end='01/01/2050')
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['Ranger'] = range(len(s))
window = 34 #minimum practical window days is probably 5
s['NDayHigh'] = s['Adj Close'].rolling(center=False, window=window).max()
s.loc[:,'NDayHigh'] = s['NDayHigh'].fillna(0)
s.loc[:,'NDayHigh'][:window-1]  = s.loc[:,'NDayHigh'][window]
s['NDayLow'] = s['Adj Close'].rolling(center=False, window=window).min()
s.loc[:,'NDayLow'] = s['NDayLow'].fillna(0)
s.loc[:,'NDayLow'][:window-1] = s.loc[:,'NDayLow'][window]
s.loc[:,'Ranger'] = range(len(s))
k = pd.DataFrame()
derp = list(s['Adj Close'])
kk = pd.Series(derp,index = range(len(s)))
k['Adj Close'] = kk
listo = []
x = []
s = s[window:]
for i in s['NDayHigh']:
    x.append(i)
for xx in x:
    xxx = min(k['Adj Close'][k['Adj Close'] == xx].index)
    listo.append(xxx)
listo1 = []
y = []
for ii in s['NDayLow']:
    y.append(ii)
for yy in y:
    yyy = min(k['Adj Close'][k['Adj Close'] == yy].index)
    listo1.append(yyy)
HighIndex = pd.Series(listo,index=s.index)
LowIndex = pd.Series(listo1,index=s.index)
HighDF = pd.DataFrame(HighIndex,columns = ['HighDF'])
LowDF = pd.DataFrame(LowIndex,columns = ['LowDF'])
s = pd.concat([s, HighDF, LowDF], axis = 1)
s.loc[:,'DaysPastHigh'] = s['Ranger'] - s['HighDF']
s['DaysPastLow'] = s['Ranger'] - s['LowDF']
s['AroonUp'] = ((window - s['DaysPastHigh']) / window) * 100
s['AroonDown'] = ((window - s['DaysPastLow']) / window) * 100
z = set(s['AroonUp'])
zz = set(s['AroonDown'])
z1 = sorted(z)
zz1 = sorted(zz)
z2 = [l for l in z1 if l >= 0]
zz2 = [ll for ll in zz1 if ll >= 0]
s.loc[:,'AroonUp'][s['AroonUp'] < 0] = z2[0]
s.loc[:,'AroonDown'][s['AroonDown'] < 0] = zz2[0]
s['Divergence'] = s['AroonUp'] - s['AroonDown']
s['Touch'] = np.where(s['Divergence'] < 89.121607, 1, 0) #long signal
s['Touch'] = np.where(s['Divergence'] > 80.586518, -1, s['Touch']) #short signal
s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                            s['Sustain']) 
s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) 
s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1, 
                        s['Sustain'])
s['Sustain'] = np.where(s['Divergence'] > 36.158261, 0, s['Sustain']) 
s['Sustain'] = np.where(s['Divergence'] < 63.346901, 0, s['Sustain']) 
s['Regime'] = s['Touch'] + s['Sustain']
s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
s['Strategy'] = s['Strategy'].fillna(0)
#    s = s.drop('HighDF', 1)
#    s = s.drop('LowDF', 1)
endgains = 1
endreturns = 1
for g in s['LogRet']:
    slate = endreturns * (1+g)
    endreturns = slate
for w in s['Strategy']:
    otherslate = endgains * (1+w)
    endgains = otherslate
#if endreturns > endgains:
#    continue
#if s['Strategy'].std() == 0:
#    continue
sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
                                             figsize = (8,5))
s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))

