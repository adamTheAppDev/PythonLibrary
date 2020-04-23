# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer, code is unfinished 
#Pandas_datareader is deprecated, use YahooGrabber

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd

#Empty data structures
counter = 0
empty = [] 
dataset = pd.DataFrame()
#Number of iterations
iterations = range(0,1000) 
#Ticker assignment
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='07/01/2010', end='01/01/2050') 
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Close location values
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Calculate ADI
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
#For number of iterations
for x in iterations:
    #Number of periods in time series
    Length = len(s)
    #Iterable
    Range = range(0,Length-1)        
    #Iteration tracking
    counter = counter + 1    
    #Generate random params
    aa = rand.randint(1,30)
    bb = rand.randint(2,60)
    #Constraints
    if aa > bb:
        continue
    #Generate random params   
    c = rand.randint(2,60)
    d = 2 - rand.random() * 4
    e = 2 - rand.random() * 4
    f = 2 - rand.random() * 4
    g = 2 - rand.random() * 4
    a = aa #number of days for moving average window
    b = bb #numer of days for moving average window
    #Assign ADI
    values = s['ADI']
    #Prep EMA weights
    weights = np.repeat(1.0, a)/a
    weights2 = np.repeat(1.0, b)/b
    #Calculate EMAs
    smas = np.convolve(values, weights, 'valid')
    smas2 = np.convolve(values, weights2, 'valid')
    #Time series trimmer
    trim = len(s) - len(smas2)
    trim2 = len(smas) - len(smas2)
    #Data to add back later 
    replace = s[:trim]
    s = s[trim:]
    smas = smas[trim2:]
    #EMAs to dataframe
    s['ADIEMAsmall'] = smas
    s['ADIEMAlarge'] = smas2
    s = replace.append(s)
    volumewindow = c
    #Calculate average rolling volume
    s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
    #Calculate Chaikin indicator
    s.loc[:,'Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    #Normalize by volume
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
    #Add data back
    s = kk.append(s)
    #Constraint
    if s['Strategy'].std() == 0:
        continue
    #Performance metric
    sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    #Constraints
    if np.isnan(sharpe) == True:
        continue
    if sharpe < 0.00001:
        continue
    #Save params and metrics to list
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
    #Iteration tracking
    print(counter)
#Metric of choice    
z1 = dataset.iloc[7]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your paramss for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold 
    if h > w1:
      #Add to list
      v1.append(h)
#For all top metrics      
for j in v1:
      #Get column ID of top metric
      r = dataset.columns[(dataset == j).iloc[7]]    
      #Save param set to dataframe
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
