# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:37:33 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
from pandas_datareader import data
import pandas as pd
import time as t
import random as rand
empty = [] #reusable list
#set up desired number of datasets for different period analysis
dataset1 = pd.DataFrame()
start = t.time()
ticker = 'SPY'
q = data.DataReader(ticker, 'yahoo', start='01/01/2013', end='01/01/2050')
q['LogRet'] = np.log(q['Adj Close']/q['Adj Close'].shift(1)) 
q['LogRet'] = q['LogRet'].fillna(0)
q['Ranger'] = range(len(q))
iterations = range(0,500) 
start = t.time() #for timing purposes un-comment this line and lines 50-51
for i in iterations:
    s = pd.DataFrame()
    s = q
    a = rand.randint(5,100)
    b = 100 - rand.random() * 200
    c = 100 - rand.random() * 200
    d = 100 - rand.random() * 200
    e = 100 - rand.random() * 200
    window = a #minimum practical window days is probably 5
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
    s['Touch'] = np.where(s['Divergence'] < b, 1, 0) #long signal
    s['Touch'] = np.where(s['Divergence'] > c, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                            s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1, 
                        s['Sustain'])
    s['Sustain'] = np.where(s['Divergence'] > d, 0, s['Sustain']) 
    s['Sustain'] = np.where(s['Divergence'] < e, 0, s['Sustain']) 
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
    if endreturns > endgains:
        continue
    if s['Strategy'].std() == 0:
        continue
    sharpe = (s['Strategy'].mean()-abs(s['LogRet'].mean()))/s['Strategy'].std()
    if sharpe < 0.02:
        continue
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(endreturns)
    empty.append(endgains)
    empty.append(sharpe)
    emptyseries1 = pd.Series(empty)
    dataset1[i] = emptyseries1.values
    empty[:] = []   
end = t.time()
sharpies = dataset1.iloc[7]
w1 = np.percentile(sharpies, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in sharpies:
    if h > w1:
      v1.append(h)
for j in v1:
      r = dataset1.columns[(dataset1 == j).iloc[7]]    
      DS1W = pd.concat([DS1W,dataset1[r]], axis = 1)
y2 = max(sharpies)
x2 = dataset1.columns[(dataset1 == y2).iloc[7]] #this is the column number
print(dataset1[x2]) #this is the dataframe index based on column number
print('Dataset 1 is optimized, it took',end-start, 'seconds') #run time in seconds
#print(sharpe)
#s[['LogRet', 'Strategy']].cumsum().apply(np.exp).plot(grid = True,
#                                             figsize = (8,5))
#s[['AroonUp', 'AroonDown']].plot(grid=True, figsize=(8,3))