# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:39:58 2017

@author: AmatVictoriaCuramIII
"""

import numpy as np
import pandas as pd
from pandas_datareader import data
import os
os.chdir('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python')
#import pandas as pd
Aggregate = pd.read_pickle('RUTAGGSHARPE044')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
base = 0
size = len(Aggregate.iloc[0])
s = data.DataReader('^RUT', 'yahoo', start='01/01/1950', end='01/01/2050') #change to s if after 6pm 
#s2 = pd.DataFrame({'Open':[1392.03],'High':[1400.81],'Low':[1390.44],'Close':[0],'Volume':[0],
#'Adj Close':[1398.36]},index = ['2017-05-10 00:00:00']) #interday
#s = pd.concat([s,s2]) #if after 6pm then comment out
for i in Aggregate:
    a = Aggregate[i].iloc[0]
    aa = a.astype(int)
    b = Aggregate[i].iloc[1]
    c = Aggregate[i].iloc[2]
    d = Aggregate[i].iloc[3]
    e = Aggregate[i].iloc[4]
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    close = s['Adj Close']
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
    s['RSI'] = RSI
    s['RSI'] = s['RSI'].fillna(0)
    s['Touch'] = np.where(s['RSI'] < b, 1,0) #long signal
    s['Touch'] = np.where(s['RSI'] > c, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                  s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                s['Sustain']) 
    s['Sustain'] = np.where(s['RSI'] > d, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['RSI'] < e, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    toadd = s['Regime'][-1]
    base = base + toadd 
    advice = base/size
print(advice)