# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 20:59:29 2017

@author: AmatVictoriaCuramIII
"""

#This is part of a kth fold optimization tool

import numpy as np
import os
os.chdir('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python')
#import pandas as pd
def DefRSIPredictor(Aggregate, s):
    base = 0
    size = len(Aggregate.iloc[0])
#s = data.DataReader('^GSPC', 'yahoo', start='01/01/1950', end='01/01/2050') #change to s if after 6pm 
#s2 = pd.DataFrame({'Open':[0],'High':[0],'Low':[0],'Close':[0],'Volume':[0], #if after 6pm then comment out
#'Adj Close':[2380]},index = ['2017-03-28 00:00:00']) #if after 6pm then comment out
#s = pd.concat([s1,s2]) #if after 6pm then comment out
    for i in Aggregate:
        a = Aggregate[i].iloc[0]
        aa = a.astype(int)
        b = Aggregate[i].iloc[1]
        c = Aggregate[i].iloc[2]
        d = Aggregate[i].iloc[3]
        e = Aggregate[i].iloc[4]
        s.loc[:,'LogRet'] = np.log(s.loc[:,'Adj Close']/s.loc[:,'Adj Close'].shift(1)) 
        s.loc[:,'LogRet'] = s.loc[:,'LogRet'].fillna(0)
        close = s.loc[:,'Adj Close']
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
        s.loc[:,'RSI'] = RSI
        s.loc[:,'RSI'] = s.loc[:,'RSI'].fillna(0)
        s.loc[:,'Touch'] = np.where(s.loc[:,'RSI'] < b, 1,0) #long signal
        s.loc[:,'Touch'] = np.where(s.loc[:,'RSI'] > c, -1, s.loc[:,'Touch']) #short signal
        s.loc[:,'Sustain'] = np.where(s.loc[:,'Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
        s.loc[:,'Sustain'] = np.where(s.loc[:,'Sustain'].shift(1) == 1, 1, 
                                  s.loc[:,'Sustain']) 
        s.loc[:,'Sustain'] = np.where(s.loc[:,'Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
        s.loc[:,'Sustain'] = np.where(s.loc[:,'Sustain'].shift(1) == -1, -1,
                                s.loc[:,'Sustain']) 
        s.loc[:,'Sustain'] = np.where(s.loc[:,'RSI'] > d, 0, s.loc[:,'Sustain']) #if RSI is greater than threshold, sustain is forced to 0
        s.loc[:,'Sustain'] = np.where(s.loc[:,'RSI'] < e, 0, s.loc[:,'Sustain']) #never actually true when optimized
        s.loc[:,'Regime'] = s.loc[:,'Touch'] + s.loc[:,'Sustain']
        toadd = s.loc[:,'Regime'][-1]
        base = base + toadd 
        advice = base/size
    return advice
