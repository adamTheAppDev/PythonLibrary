# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#Pandas_datareader is deprecated, use YahooGrabber
#This is a brute force optimizer with a strategy tester

#Import modules
import numpy as np
from pandas_datareader import data
import random as rand
import pandas as pd
import time as t

#Empty data structures
empty = [] 
dataset = pd.DataFrame()
counter = 0
store = 0
ADI = []
#Assign ticker
ticker = '^GSPC'
#Number of iterations
iterations = range(0,2500)

#Request data
s = data.DataReader(ticker, 'yahoo', start='07/01/2013', end='12/01/2016') 
#Calculate log returns
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0)
#Prerp for NC indicator
s['CLV'] = (((s['Adj Close'] - s['Low']) - (s['High'] - s['Adj Close']))
                    / (s['High'] - s['Low']))
#Length of time series
Length = len(s['LogRet'])
#Iterable
Range = range(0,Length)
#Assign index to variable
index = s.index
#For number of days in time series
for i in Range:
        #Temp variable
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
    #Constraint
    if aa > bb:
        continue
    #Generate random params
    c = rand.randint(2,60)
    d = rand.randint(2,60)
    e = 2 - rand.random() * 4
    f = 2 - rand.random() * 4
    g = 2 - rand.random() * 4
    h = 2 - rand.random() * 4
    a = aa #number of days for moving average window
    b = bb #numer of days for moving average window
    #EMA prep
    multiplierA = (2/(a+1))
    multiplierB = (2/(b+1))
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
    volumewindow = c
    #Calculate average rolling volume
    s['AverageRollingVolume'] = s['Volume'].rolling(center=False,
                                window=volumewindow).mean()
    #Calculate chaikin indicator
    s['Chaikin'] = s['ADIEMAsmall'] - s['ADIEMAlarge']
    #Normalize for volume
    s['NormChaikin'] = s['Chaikin']/s['AverageRollingVolume']
    #SMA of indicator
    s['NormChaikinMovAvg'] = s['NormChaikin'].rolling(window=d,center=False).mean()
    #Spread between indicator and indicator SMA
    s['MovAvgDivergence'] = s['NormChaikin'] - s['NormChaikinMovAvg']
    #Directional methodology
    s['Touch'] = np.where(s['NormChaikin'] < e, 1,0) #long signal
    s['Touch'] = np.where(s['NormChaikin'] > f, -1, s['Touch']) #short signal
    s['Sustain'] = np.where(s['Touch'].shift(1) == 1, 1, 0) # never actually true when optimized
    s['Sustain'] = np.where(s['Sustain'].shift(1) == 1, 1, 
                                   s['Sustain']) 
    s['Sustain'] = np.where(s['Touch'].shift(1) == -1, -1, 0) #true when previous day touch is -1, and current RSI is > line 37 threshold 
    s['Sustain'] = np.where(s['Sustain'].shift(1) == -1, -1,
                                 s['Sustain']) 
    s['Sustain'] = np.where(s['NormChaikin'] > g, 0, s['Sustain']) #if RSI is greater than threshold, sustain is forced to 0
    s['Sustain'] = np.where(s['NormChaikin'] < h, 0, s['Sustain']) #never actually true when optimized
    s['Regime'] = s['Touch'] + s['Sustain']
    #Apply position to returns
    s['Strategy'] = (s['Regime']).shift(1)*s['LogRet']
    s['Strategy'] = s['Strategy'].fillna(0)
    #Constraints
    if s['Strategy'].std() == 0:
        continue
    #Performance metric
    sharpe = (s['Strategy'].mean()-s['LogRet'].mean())/s['Strategy'].std()
    #Constraint
    if sharpe < 0.001:
        continue
    #Iteration tracking    
    print(counter)
    #Save params and metric to list
    empty.append(a)
    empty.append(b)
    empty.append(c)
    empty.append(d)
    empty.append(e)
    empty.append(f)
    empty.append(g)
    empty.append(h)
    empty.append(sharpe)
    #List to Series
    emptyseries = pd.Series(empty)
    #Series to dataframe
    dataset[x] = emptyseries.values
    #Empty list
    empty[:] = []      
#End timer    
end = t.time()
#Metric of choice
z1 = dataset.iloc[8]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics 
for z in z1:
    #If greater than threshold
    if z > w1:
      #Add to list
      v1.append(z)
#For top metrics      
for j in v1:
      #Get column ID of metric
      r = dataset.columns[(dataset == j).iloc[8]]    
      #Add param set to dataframe
      DS1W = pd.concat([DS1W,dataset[r]], axis = 1)
#Top metric      
y = max(z1)
#Column ID of top metric
k = dataset.columns[(dataset == y).iloc[8]]
#Display top param set
print(dataset[k])
#Timer stats
print('Time = ',end-start)
