  
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

#Empty data structures
Empty = []
Dataset = pd.DataFrame()
Portfolio = pd.DataFrame()
Counter = 0

#Start timer
Start = t.time()

#Assign tickers
Ticker1 = 'UVXY'
Ticker2 = '^VIX'
Ticker3 = '^VIX'
Ticker4 = '^VXV'

#Request data
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = YahooGrabber(Ticker3)
Asset4 = YahooGrabber(Ticker4)

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
Asset4 = Asset4[-len(Asset2):]

#Calculate log returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Price relative
Asset3['Meter'] = (Asset3['Close']/Asset4['Close'])

#Number of iterations for Brute Force Optimization
iterations = range(0, 200000)

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
    if c + d > 1: continue
    e = 1.5 - (rand.random()*1)
    #Generate random params
    f = rand.randint(3,30)
    g = rand.randint(0,30)
    window2 = int(f)
    window3 = int(g)
    #Directional methodology
    Asset3['Signal'] = np.where(Asset3['Meter'].shift(1) > e, 1, 0)
    #Sum of signals in windowed period
    Asset3['CumulativeRollingSignal'] = Asset3['Signal'].rolling(window = window2).sum()
    #Position sizing
    Asset1['Position'] = a
    #Alternative position sizing
    Asset1['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3, c, a)  
    #Apply position to returns
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    #Position sizing
    Asset2['Position'] = b
    #Alternative position sizing
    Asset2['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3, d, b) 
    #Apply position to returns
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    #Pass individual return streams to portfolio
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
    #Cumulative returns
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass'])  
    #Constraint
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown
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
    #Performance metrics
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Iteration tracking
    print(Counter)
    #Save params to list
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
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[i] = Emptyseries.values
    #Clear list
    Empty[:] = [] 
#Metric of choice    
z1 = Dataset.iloc[8]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For all metrics
for h in z1:
    #If greater than threshold
    if h > w1:
      #Add to list  
      v1.append(h)
#For top metrics        
for j in v1:
      #Get column ID of metric
      r = Dataset.columns[(Dataset == j).iloc[8]]    
      #Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[8]]
#Column ID of top metric - float
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])

#Read in params
window = (Dataset[kfloat][4])
window2 = int(Dataset[kfloat][5])
window3 = int(Dataset[kfloat][6])
#Directional methodology
Asset3['Signal'] = np.where(Asset3['Meter'].shift(1) > Dataset[kfloat][4], 1, 0)
#Sum of signals in window period
Asset3['CumulativeRollingSignal'] = Asset3['Signal'].rolling(window = window2).sum()
#Position sizing
Asset1['Position'] = Dataset[kfloat][0]
#Alternative position sizing
Asset1['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3,
                                     Dataset[kfloat][2], Dataset[kfloat][0])   
#Apply position to returns
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
#Position sizing
Asset2['Position'] = Dataset[kfloat][1]
#Alternative position sizing
Asset2['SmartPosition'] = np.where(Asset3['CumulativeRollingSignal'] > window3,
                                     Dataset[kfloat][3], Dataset[kfloat][1]) 
#Apply position to returns
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
#Pass individual return streams to portfolio
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Cumulative returns
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True, figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#Display results
print(max(drawdown2))
#Save to pickle
#pd.to_pickle(Portfolio, 'VXX:UVXY')
