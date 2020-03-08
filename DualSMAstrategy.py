# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a brute force optimization single asset strategy tester

import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
from pandas import read_csv
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Input ticker
Ticker1 = 'UVXY'
#Ticker2 = '^VIX'

#Daily UVXY
Asset1 = YahooGrabber(Ticker1)

#Out of Sample Selection
#Asset1 = Asset1[:-800]

#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Brute Force Optimization - number of iterations
iterations = range(0, 10000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Variable assignments
    a = 1
    b = rand.randint(8,50) #small MA
    c = rand.randint(8,500) #big MA
    #Constraint
    if b >= c:
        continue
    #Moving averages
    window = int(b)
    window2 = int(c)
    #SMA calculation
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean() #small
    Asset1['MA2'] = Asset1['Adj Close'].rolling(window=window2, center=False).mean() #big
    #Directional methodology
    Asset1['Regime'] = np.where(Asset1['MA'] > Asset1['MA2'], 1 , -1)                                 
    Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'])
    
    #Constraint
    #if Asset1['Strategy'].std() == 0:    
    #    continue
    #Returns on $1
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    #Spurious drawdown statistic
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Drawdown constraint
#    if MaxDD > float(.721): 
#            continue
    #Performance statistic
    dailyreturn = Asset1['Strategy'].mean()
    #Constraint
    #    if dailyreturn < .003:
    #        continue
    #Performance statistics
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
    
    #Iteration tracking
    print(Counter)
    #Saving params + stats to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    
    #List to series to DataFrame
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
#All desired performance statistics    
z1 = Dataset.iloc[3]
#Top n percentile threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performing stats
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If metric above param threshold
    if h > w1:
      #add metric to list
      v1.append(h)
#For all top metrics
for j in v1:
      #Find params by metric
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      #Add params to DataFrame
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#This is optimal param
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])

#End timer
End = t.time()
#Time stats
print(End-Start, 'seconds later')
#Optimal param set
print(Dataset[k])

#Testing optimal param set
#SMA window
window = int((Dataset[kfloat][1]))
window2 = int((Dataset[kfloat][2]))
#SMA calculation
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean() #small MA
Asset1['MA2'] = Asset1['Adj Close'].rolling(window=window2, center=False).mean() #big MA
#Directional methodology
Asset1['Regime'] = np.where(Asset1['MA'] > Asset1['MA2'], 1 , -1)
#Strategy returns 
Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'])
#Display
Asset1['Strategy'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance statistics
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()
sharpe = (dailyreturn / dailyvol)
#Returns on $1
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
#Spurious drawdown statistic
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
print(max(drawdown))
