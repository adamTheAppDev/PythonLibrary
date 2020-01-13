# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:41:57 2017

@author: AmatVictoriaCuramIII
"""

#This is part of a kth fold optimization
#Pandas_datareader is deprecated, use YahooGrabber

import numpy as np
import pandas as pd
from pandas_datareader import data
import os
os.chdir('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python')
#import pandas as pd
Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
base = 0
size = len(Aggregate.iloc[0])
ticker = '^GSPC'
s = data.DataReader(ticker, 'yahoo', start='07/01/1983', end='01/01/2050')
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
values = s['ADI']
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0) #change to s if after 6pm 
#s2 = pd.DataFrame({'Open':[0],'High':[0],'Low':[0],'Close':[0],'Volume':[0], #if after 6pm then comment out
#'Adj Close':[2380]},index = ['2017-03-28 00:00:00']) #if after 6pm then comment out
#s = pd.concat([s1,s2]) #if after 6pm then comment out
for i in Aggregate:
    aa = Aggregate.loc[0,i] #numer of days for moving average window
    a = aa.astype(int)
    bb = Aggregate.loc[1,i] #numer of days for moving average window
    b = bb.astype(int)
    cc = Aggregate.loc[2,i] #numer of days for volume window
    c = cc.astype(int)
    d = Aggregate[i].iloc[3] 
    e = Aggregate[i].iloc[4]
    f = Aggregate[i].iloc[5]
    g = Aggregate[i].iloc[6]
    weights = np.repeat(1.0, a)/a
    weights2 = np.repeat(1.0, b)/b
    smas = np.convolve(values, weights, 'valid')
    smas2 = np.convolve(values, weights2, 'valid')
    trim = len(s) - len(smas2)
    trim2 = len(smas) - len(smas2)
    replace = s[:trim]
    s = s[trim:]
    smas = smas[trim2:]
    s['ADIEMAsmall'] = smas
    s['ADIEMAlarge'] = smas2
    s = replace.append(s)
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
    toadd = s['Regime'][-1]
    base = base + toadd 
    advice = base/size
    s = kk.append(s)
print(advice)
