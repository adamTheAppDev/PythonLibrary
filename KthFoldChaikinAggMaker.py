# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#pandas_datareader is deprecated, use YahooGrabber
#This is part of a kth fold optimization tool with Chaikin technical indicator

#Import modules
import numpy as np
import pandas as pd
import time as t
from pandas_datareader import data

#Empty data structures
empty = []
openspace = []
openseries = pd.Series()
testsetwinners = pd.DataFrame()

#define function
def ChaikinAggMaker(ticker, testset, firsttime, secondtime):
    #Request data
    s = data.DataReader(ticker, 'yahoo', start=firsttime, end=secondtime)
    #Calculate log returns
    s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
    s['LogRet'] = s['LogRet'].fillna(0)
    #ADI calculation
    s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                        / (s['High'] - s['Low']))
    s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
    #Start timer
    starttime = t.time()
    For params in testset
    for i in testset:       
        #Load params
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
        #Assign variables
        values = s['ADI']
        weights = np.repeat(1.0, a)/a
        weights2 = np.repeat(1.0, b)/b
        #SMA calculation
        smas = np.convolve(values, weights, 'valid')
        smas2 = np.convolve(values, weights2, 'valid')
        #Trim time series
        trim = len(s) - len(smas2)
        trim2 = len(smas) - len(smas2)
        replace = s[:trim]
        s = s[trim:]
        smas = smas[trim2:]
        #ADI EMA values
        s['ADIEMAsmall'] = smas
        s['ADIEMAlarge'] = smas2
        s = replace.append(s)
        volumewindow = c
        #Average rolling volume
        s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                            window=volumewindow).mean()
        #Calculate chaikin indicator
        s.loc[:,'Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
        s.loc[:,'NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
        #Trim time series
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
        #Redundance
        s = kk.append(s)
        #Constraints
        if s['Strategy'].std() == 0:
            continue
        #Performance metric
        sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
        #Constraints
        if np.isnan(sharpe) == True:
            continue
        if sharpe < 0.0205:
                continue
        #Add params and metrics to list        
        openspace.append(a)
        openspace.append(b)
        openspace.append(c)
        openspace.append(d)
        openspace.append(e)
        openspace.append(f)
        openspace.append(g)
        openspace.append(sharpe)
        #List to Series
        openseries = pd.Series(openspace)
        #Series to dataframe
        testsetwinners[i] = openseries.values
        #Clear list
        openspace[:] = []
    #End timer
    endtime = t.time()
    #Timer stats
    print('That dataset took ', endtime-starttime,' seconds')  
    #Output optimal params
    return testsetwinners
