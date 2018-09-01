# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:01:58 2017

@author: AmatVictoriaCuramIII
"""
def DefNormChaikinStratOpt(ticker,start,end):
    import numpy as np
    from pandas_datareader import data
    import random as rand
    import pandas as pd
    empty = [] #reusable list
    #set up desired number of datasets for different period analysis
    dataset = pd.DataFrame()
    iterations = range(0,1000)
    ticker = '^GSPC'
    s = data.DataReader(ticker, 'yahoo', start=start, end=end) 
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                        / (s['High'] - s['Low']))
    s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
    for x in iterations:       
        aa = rand.randint(1,30)
        bb = rand.randint(2,60)
        if aa > bb:
            continue
        c = rand.randint(2,60)
        d = 5.5 - rand.random() * 7
        e = 5.5 - rand.random() * 7
        f = 5.5 - rand.random() * 7
        g = 5.5 - rand.random() * 7
        a = aa #number of days for moving average window
        b = bb #numer of days for moving average window
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
        if sharpe < 0.001:
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
    z1 = dataset.iloc[7]
    w1 = np.percentile(z1, 70)
    v1 = [] #this variable stores the Nth percentile of top performers
    DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
    for h in z1:
        if h > w1:
          v1.append(h)
    for j in v1:
          r = dataset.columns[(dataset == j).iloc[7]]    
          DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
    return DS1W