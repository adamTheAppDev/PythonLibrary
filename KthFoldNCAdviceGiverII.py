# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is part of a kth fold optimization
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
import pandas as pd
from pandas_datareader import data
import os

#import pandas as pd
#Read in data
Aggregate = pd.read_pickle('SP500NCAGGSHARPE0205')
Aggregate = Aggregate.loc[:,~Aggregate.columns.duplicated()]
#Zeros
base = 0
#Read in params
size = len(Aggregate.iloc[0])
#Ticker assignment
ticker = '^GSPC'
#Read in data
s = data.DataReader(ticker, 'yahoo', start='07/01/1983', end='01/01/2050')
#Calculate ADI
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
values = s['ADI']
#Calculate log return
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0) #change to s if after 6pm
#Add new data for prediction on close
#s2 = pd.DataFrame({'Open':[0],'High':[0],'Low':[0],'Close':[0],'Volume':[0], #if after 6pm then comment out
#'Adj Close':[2380]},index = ['2017-03-28 00:00:00']) #if after 6pm then comment out
#s = pd.concat([s1,s2]) #if after 6pm then comment out
#For all param sets
for i in Aggregate:
    #Read in params
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
    #Weights for EMA
    weights = np.repeat(1.0, a)/a
    weights2 = np.repeat(1.0, b)/b
    #EMAs
    smas = np.convolve(values, weights, 'valid')
    smas2 = np.convolve(values, weights2, 'valid')
    #Time series trimming
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
    #Assign params
    volumewindow = c
    #Calculate rolling volume
    s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
    #Calculate normalized Chaikin indicator
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
    #Param sets directional assumption
    toadd = s['Regime'][-1]
    #Add to aggregate params directional assumption
    base = base + toadd 
    #total aggregate params directional assumption
    advice = base/size
    #Add data to list
    s = kk.append(s)
#Display aggregate params directional assumption
print(advice)
