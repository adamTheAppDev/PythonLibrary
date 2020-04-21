# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a strategy tester with a brute force optimizer
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
#Assign ticker
ticker = '^GSPC'
#Request data
s = data.DataReader(ticker, 'yahoo', start='07/01/2010', end='01/01/2050') 
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Calculate close location value
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Calculate ADI
s['ADI'] = (s['Volume'] * s['CLV']).cumsum()
#For number of iterations
for x in iterations:
    #Number of periods in time series
    Length = len(s)
    Range = range(0,Length-1)        
    #Iteration tracking
    counter = counter + 1    
    #Generate random params
    aa = rand.randint(1,30)
    bb = rand.randint(2,60)
    #Constraint
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
    #Prer EMA
    multiplierA = (2/(a+1))
    multiplierB = (2/(b+1))
    #Initialize values
    EMAyesterdayA = s['ADI'][0] 
    EMAyesterdayB = s['ADI'][0] 
    #Calculate small EMA
    smallEMA = [EMAyesterdayA]
    for i in Range:
        holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
        smallEMA.append(holder)
        EMAyesterdayA = holder
    smallEMAseries = pd.Series(smallEMA[:], index=s.index)    
    #Calculate large EMA
    largeEMA = [EMAyesterdayB]
    for i in Range:
        holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
        largeEMA.append(holder1)
        EMAyesterdayB = holder1
    largeEMAseries = pd.Series(largeEMA[:], index=s.index)
    #Add to dataframe
    s.loc[:,'ADIEMAsmall'] = smallEMAseries
    s.loc[:,'ADIEMAlarge'] = largeEMAseries
    #Param assignment
    volumewindow = c
    #Average rollng volume
    s.loc[:,'AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
    #Calculate Chaikin indicator
    s.loc[:,'Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    #Normalize by volume
    s.loc[:,'NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
    #Time series trim
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
    #Empty list
    empty[:] = []      
    #Iteration tracking
    print(counter)
#Metric of choice    
z1 = dataset.iloc[7]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #This variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top metrics      
for j in v1:
      #Find column ID of metric
      r = dataset.columns[(dataset == j).iloc[7]]  
      #Add to dataframe
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
