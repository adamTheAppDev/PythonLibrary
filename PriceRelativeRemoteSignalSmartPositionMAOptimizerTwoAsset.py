# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a two asset portfolio/strategy tester with a brute force optimizer

#Import modules 
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Assign input
Ticker1 = 'UVXY'
Ticker2 = '^VIX'

Ticker3 = '^VIX'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = YahooGrabber(Ticker3)

#Time series trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Match lengths
Asset3 = Asset3[-len(Asset2):]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Number of iterations for Brute Force Optimization
iterations = range(0, 300000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a = rand.random()
    b = 1 - a
    c = rand.random()
    d = rand.random()
    #Constraint
    if c + d > 1:
        continue
    #Generate random params    
    e = rand.randint(3,30)
    f = rand.randint(3,30)
    g = rand.randint(0,30)
    #Assign params
    window = int(e)
    window2 = int(f)
    window3 = int(g)
    #SMA
    Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
    #Directional methodology
    Asset3['Signal'] = np.where(Asset3['MA'].shift(1) > Asset3['Adj Close'].shift(1),
                                                         1, 0)
    #Number of signals in window period
    Asset3['CumulativeRollingSignal'] = Asset3['Signal'].rolling(window = window2).sum()
    #Position sizing
    Asset1['Position'] = a
    #Alternate position sizing
    Asset1['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3, c, a)                                 
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    
    #Position sizing
    Asset2['Position'] = b
    #Alternate position sizing
    Asset2['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3, d, b) 
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

    #Pass returns to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
    #Cumulative returns
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']) 
    #    Portfolio['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                         figsize=(8,5))  
    #Constraints
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated drawdown 
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.3): 
        continue
    #Performance metric
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
    if dailyreturn < .002:
        continue
    #Performance metric
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)
    #Save params and metric to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)
    Empty.append(f)
    Empty.append(g)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to Series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
#Metric of choice    
z1 = Dataset.iloc[8]
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
#For top metric        
for j in v1:
      #Column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[8]]    
      # Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[8]] 
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Display top param set
print(Dataset[k])

#Read in params
window = int((Dataset[kfloat][4]))
window2 = int((Dataset[kfloat][5]))
#SMA
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
#Number of signals in window period
Asset3['CumulativeRollingSignal'] = Asset3['Signal'].rolling(window = window2).sum()
#Position sizing
Asset1['Position'] = Dataset[kfloat][0]
#New position size
Asset1['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > Dataset[kfloat][5],
                            Dataset[kfloat][2], Dataset[kfloat][0]) 
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = Dataset[kfloat][1]
#New position size
Asset2['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > Dataset[kfloat][5],
                            Dataset[kfloat][3], Dataset[kfloat][1]) 
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass individual return streams to portfolio
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Cumulative returns
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Display results
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metric
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated drawdown
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#Display results
print(max(drawdown2))
#Save to pickle
#pd.to_pickle(Portfolio, 'VXX:UVXY')
