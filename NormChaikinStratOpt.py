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
import time as t

#Empty structures
empty = [] 
ADI = []
dataset = pd.DataFrame()
counter = 0
store = 0
#Assign ticker
ticker = '^GSPC'
#Number of iterations
iterations = range(0,20000)
#Request data
s = data.DataReader(ticker, 'yahoo', start='07/01/2013', end='12/01/2017') 
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Close location value
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Time series
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length)
#Index object
index = s.index
#For all periods in time series
for i in Range:
        #Temporary variable
        store = store + (s['Volume'][i] * s['CLV'][i])
        #Add to list
        ADI.append(store)
#List to series        
ADISeries = pd.Series(ADI, index=index)
#Series to dataframe
s['ADI'] = ADISeries
#Start timer
start = t.time()
#For number of iterations
for x in iterations:
    #Iteration tracking
    counter = counter + 1    
    #Generate random params
    aa = rand.randint(1,30)
    bb = rand.randint(2,60)
    #Constraints
    if aa > bb:
        continue
    #Generate random params
    c = rand.randint(2,30)
    d = 2 - rand.random() * 4
    e = 2 - rand.random() * 4
    f = 2 - rand.random() * 4
    g = 2 - rand.random() * 4
    a = aa #number of days for moving average window
    b = bb #numer of days for moving average window
    multiplierA = (2/(a+1))
    multiplierB = (2/(b+1))
    #Initialize SMA values
    EMAyesterdayA = s['ADI'][0] #these prices are based off the SMA values
    EMAyesterdayB = s['ADI'][0] #these prices are based off the SMA values
    #Calculate small EMA
    smallEMA = [EMAyesterdayA]
    for i in Range:
        holder = (s['ADI'][i]*multiplierA) + (EMAyesterdayA *
                                            (1-multiplierA))
        smallEMA.append(holder)
        EMAyesterdayA = holder
    smallEMAseries = pd.Series(smallEMA[1:], index=s.index)   
    #Calculate large EMA
    largeEMA = [EMAyesterdayB]
    for i in Range:
        holder1 = (s['ADI'][i]*multiplierB) + (EMAyesterdayB *
                                            (1-multiplierB))
        largeEMA.append(holder1)
        EMAyesterdayB = holder1
    largeEMAseries = pd.Series(largeEMA[1:], index=s.index)
    #Series to dataframe
    s['ADIEMAsmall'] = smallEMAseries
    s['ADIEMAlarge'] = largeEMAseries
    #Calculate Chaikin indicator
    s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    #Horizonal line
    s['ZeroLine'] = 0
    volumewindow = c
    #Calculate average rolling volume
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                        window=volumewindow).mean()
    #Normalize by volume
    s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
    #Graphical display
    #s[['ADI','ADIEMAsmall','ADIEMAlarge']].plot(grid=True, figsize = (8,3))
    #s = s[volumewindow-1:]
    #s[['NormChaikin','ZeroLine']].plot(grid=True, figsize = (8,3))
    #Directional methodology
    s['Touch'] = np.where(s['NormChaikin'] < d, 1,0) #long signal
    s['Touch'] = np.where(s['NormChaikin'] > e, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                   s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
    s['Sustain'] = np.where(s['NormChaikin'] > f, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['NormChaikin'] < g, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    #Apply position to log returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].illna(0)
    #Constraints
    if s['Strategy'].std() == 0:
        continue
    #Performance metric    
    sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    #Constraint
    if sharpe < 0.02:
        continue
    #Iteration tracking    
    print(counter)
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
#End timer    
end = t.time()
#Metric of choice
z1 = dataset.iloc[7]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If metric greater than threshold
    if h > w1:
      #Add to list
      v1.append(h)
#For top metrics      
for j in v1:
      #Get column ID of metric
      r = dataset.columns[(dataset == j).iloc[7]]    
      #Add param set to dataframe
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Top metric      
y = max(z1)
#Column ID of top metric
k = dataset.columns[(dataset == y).iloc[7]]
#Top param set
print(dataset[k])

print('Time = ',end-start)
