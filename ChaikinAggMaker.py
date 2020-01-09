# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:24:54 2017

@author: AmatVictoriaCuramIII
"""

#This is part of a kth fold optimization tool with Chaikin technical indicator

#multiperiod tester
import numpy as np
import pandas as pd
import time as t
from pandas_datareader import data
empty = []
openspace = []
openseries = pd.Series()
testsetwinners = pd.DataFrame()
def ChaikinAggMaker(ticker, testset, firsttime, secondtime):
    s = data.DataReader(ticker, 'yahoo', start=firsttime, end=secondtime)
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                        / (s['High'] - s['Low']))
    s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
    starttime = t.time()
    for i in testset:       
        aa = testset.loc[0,i] #numer of days for moving average window
        a = aa.astype(int)
        bb = testset.loc[1,i] #numer of days for moving average window
        b = bb.astype(int)
        cc = testset.loc[2,i] #numer of days for volume window
        c = cc.astype(int)
        d = testset[i].iloc[3] 
        e = testset[i].iloc[4]
        f = testset[i].iloc[5]
        g = testset[i].iloc[6]
        values = s['ADI']
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
        s.loc[:,'Strategy'] = (s['Regime']).shift(1)*s['LogRet']
        s.loc[:,'Strategy'] = s['Strategy'].fillna(0)
        s = kk.append(s)
        if s['Strategy'].std() == 0:
            continue
        sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
        if np.isnan(sharpe) == True:
            continue
        if sharpe < 0.0205:
                continue
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(f)
        openspace.append(g)
        openspace.append(sharpe)
        openseries = pd.Series(openspace)
        testsetwinners[i] = openseries.values
        openspace[:] = []
    endtime = t.time()
    print('That dataset took ', endtime-starttime,' seconds')    
    return testsetwinners
