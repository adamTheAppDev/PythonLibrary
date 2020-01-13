# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 02:25:29 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester with a brute force optimizer
#Pandas_datareader is deprecated, use YahooGrabber

import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
empty = [] #reusable list
#set up desired number of datasets for different period analysis
dataset = pd.DataFrame()
iterations = range(0,1000)
counter = 0 
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='07/01/2010', end='01/01/2050') 
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
for x in iterations:
    Length = len(s)
    Range = range(0,Length-1)        
    counter = counter + 1    
    aa = rand.randint(1,30)
    bb = rand.randint(2,60)
    if aa > bb:
        continue
    c = rand.randint(2,60)
    d = 2 - rand.random() * 4
    e = 2 - rand.random() * 4
    f = 2 - rand.random() * 4
    g = 2 - rand.random() * 4
    a = aa #number of days for moving average window
    b = bb #numer of days for moving average window
    multiplierA = (2/(a+1))
    multiplierB = (2/(b+1))
    EMAyesterdayA = s['ADI'][0] 
    EMAyesterdayB = s['ADI'][0] 
    smallEMA = [EMAyesterdayA]
    for i in Range:
        holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
        smallEMA.append(holder)
        EMAyesterdayA = holder
    smallEMAseries = pd.Series(smallEMA[:], index=s.index)    
    largeEMA = [EMAyesterdayB]
    for i in Range:
        holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
        largeEMA.append(holder1)
        EMAyesterdayB = holder1
    largeEMAseries = pd.Series(largeEMA[:], index=s.index)
    s.loc[:,'ADIEMAsmall'] = smallEMAseries
    s.loc[:,'ADIEMAlarge'] = largeEMAseries
    volumewindow = c
    s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
    
    s.loc[:,'Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    s.loc[:,'NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
    kk = s[:volumewindow-1]        
    s = s[volumewindow-1:]        
    s.loc[:,'Touch'] = np.where(s['NormChaikin'] < d, 1,0) #long signal
    s.loc[:,'Touch'] = np.where(s['NormChaikin'] > e, -1, s['Touch']) #short signal
    s.loc[:,'Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s.loc[:,'Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                     s['Sustain']) 
    s.loc[:,'Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s.loc[:,'Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                     s['Sustain']) 
    s.loc[:,'Sustain'] = np.where(s['NormChaikin'] > f, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s.loc[:,'Sustain'] = np.where(s['NormChaikin'] < g, 0, s['Sustain']) #never actually true when optimized
    s.loc[:,'Regime'] = s['Touch'] + s['Sustain']
    s.loc[:,'Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s.loc[:,'Strategy'] = s['Strategy'].fillna(0)
    s = kk.append(s)
    if s['Strategy'].std() == 0:
        continue
    sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    if np.isnan(sharpe) == True:
        continue
    if sharpe < 0.00001:
        continue
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(g)
    empty.append(sharpe)
    emptyseries = pd.Series(empty)
    dataset[x] = emptyseries.values
    empty[:] = []      
    print(counter)
z1 = dataset.iloc[7]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = dataset.columns[(dataset == j).iloc[7]]    
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
