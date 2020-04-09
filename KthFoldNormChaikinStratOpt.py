# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimization tool that is part of a kth fold optimization tool

#Define function
def DefNormChaikinStratOpt(ticker,start,end):
    #Import modules
    import numpy as np
    from pandas_datareader import data
    import random as rand
    import pandas as pd
    #Empty structures
    empty = []
    dataset = pd.DataFrame()
    #Set up desired number of datasets for different period analysis
    #Number of iterations
    iterations = range(0,1000)
    #Assign ticker
    ticker = '^GSPC'
    #Request data
    s = data.DataReader(ticker, 'yahoo', start=start, end=end) 
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    #Calculate ADI
    s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                        / (s['High'] - s['Low']))
    s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
    #For number of iterations
    for x in iterations:     
        #Generate random params
        aa = rand.randint(1,30)
        bb = rand.randint(2,60)
        #Constraints
        if aa > bb:
            continue
        #Generate random params
        c = rand.randint(2,60)
        d = 5.5 - rand.random() * 7
        e = 5.5 - rand.random() * 7
        f = 5.5 - rand.random() * 7
        g = 5.5 - rand.random() * 7
        a = aa #number of days for moving average window
        b = bb #numer of days for moving average window
        #Variable assignment
        values = s['ADI']
        #Assign EMA weights
        weights = np.repeat(1.0, a)/a
        weights2 = np.repeat(1.0, b)/b
        #EMAs
        smas = np.convolve(values, weights, 'valid')
        smas2 = np.convolve(values, weights2, 'valid')
        #Time series trimmer 
        trim = len(s) - len(smas2)
        trim2 = len(smas) - len(smas2)
        replace = s[:trim]
        s = s[trim:]
        smas = smas[trim2:]
        #EMAs
        s['ADIEMAsmall'] = smas
        s['ADIEMAlarge'] = smas2
        #Add data
        s = replace.append(s)
        #Param assignment
        volumewindow = c
        #Average rolling volume calculation
        s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                            window=volumewindow).mean()
        #Calculate normalized Chaikin indicator
        s.loc[:,'Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
        s.loc[:,'NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
        #Time series trimming
        kk = s[:volumewindow-1]        
        s = s[volumewindow-1:]        
        #Directional methodology
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
        #Apply position to returns
        s.loc[:,'Strategy'] = (s['Regime']).shift(1)*s['LogRet']
        s.loc[:,'Strategy'] = s['Strategy'].fillna(0)
        #Add data
        s = kk.append(s)
        #Constraints
        if s['Strategy'].std() == 0:
            continue
        #Performance metrics
        sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
        #Constraints
        if np.isnan(sharpe) == True:
            continue
        if sharpe < 0.001:
            continue
        #Add params and metrics to list
        empty.append(a)
        empty.append(b)
        empty.append(c)
        empty.append(d)
        empty.append(e)
        empty.append(f)
        empty.append(g)
        empty.append(sharpe)
        #List to series
        emptyseries = pd.Series(empty)
        #Series to dataframe
        dataset[x] = emptyseries.values
        #Clear list
        empty[:] = []
    #Metric of choice
    z1 = dataset.iloc[7]
    #Threshold
    w1 = np.percentile(z1, 70)
    v1 = [] #this variable stores the Nth percentile of top params
    DS1W = pd.DataFrame() #this variable stores your params for specific dataset
    #For all metrics
    for h in z1:
        #If greater than threshold
        if h > w1:
          #Add to list
          v1.append(h)
    #For top metrics
    for j in v1:
          #Get column number/ID
          r = dataset.columns[(dataset == j).iloc[7]]    
          #Add to dataframe by column ID
          DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
    #Output top params
    return DS1W
