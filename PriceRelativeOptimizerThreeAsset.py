# -*- coding: utf-8 -*-
"""

@author: Adam Reinhold Von Fisher - https://www.linkedin.com/in/adamrvfisher/

"""

#This is a three asset portfolio/strategy tester with a brute force optimizer

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
Ticker2 = 'VXX'
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

#Trim
Asset3 = Asset3[-len(Asset2):]

#Calculate log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#Number of iterations - Brute Force Optimization
iterations = range(0, 4000)
#For number of iterations
for i in iterations:
    #Iteration tracking
    Counter = Counter + 1
    #Generate random params
    a1 = rand.random()
    b1 = rand.random()
    c1 = rand.random()
    total = a1 + b1 + c1
    a = a1/total
    b = b1/total
    #Constraint
    if b > .3:
        continue
    c = c1/total
    #Position sizing // apply position to returns
    Asset1['Position'] = a
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Asset3['Position'] = c
    Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
    #Individual return streams
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass'])
    Portfolio['Asset3Pass'] = (Asset3['Pass'])
#    Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
    #asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
    #Cumulative returns
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']
                               + Portfolio['Asset3Pass']) 
    #    Portfolio['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                         figsize=(8,5))  
    #Constraints
    if Portfolio['LongShort'].std() == 0:    
        continue
    #Returns on $1
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    #Incorrectly calculated max drawdown stat
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    #Constraint
    if MaxDD > float(.27): 
        continue
    #Performance metric
    dailyreturn = Portfolio['LongShort'].mean()
    #Constraint
    if dailyreturn < .0035:
        continue
    #Performance metric
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    #Incorrectly calculated max drawdown stat
    MaxDD = max(drawdown)
    #Iteration tracking
    print(Counter)
    #Save params and metric to list
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    #List to series
    Emptyseries = pd.Series(Empty)
    #Series to dataframe
    Dataset[i] = Emptyseries.values
    #Empty list
    Empty[:] = [] 
#Metric of choice    
z1 = Dataset.iloc[4]
#Threshold
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top params
DS1W = pd.DataFrame() #this variable stores your params for specific dataset
#For metrics in list
for h in z1:
    #If metric greater than threshold
    if h > w1:
      #Add to list  
      v1.append(h)
#For top metrics        
for j in v1:
      #Get column ID
      r = Dataset.columns[(Dataset == j).iloc[4]]    
      #Add to dataframe
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
#Top metric    
y = max(z1)
#Column ID of top metric
k = Dataset.columns[(Dataset == y).iloc[4]] 
#Top param set
kfloat = float(k[0])
#End timer
End = t.time()
#Timer stats
print(End-Start, 'seconds later')
#Top param set
print(Dataset[k])

#Read in top params
#Position sizing // apply position to returns
Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Asset3['Position'] = (Dataset[kfloat][2])
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
#Individual return streams
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass']
Portfolio['Asset3Pass'] = Asset3['Pass']
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
#Cumulative returns
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']  
                            + Portfolio['Asset3Pass'])
#Graphical display
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#Performance metrics
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
#Returns on $1
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
#Incorrectly calculated max drawdown
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
print(max(drawdown2))
#Save to pickle
#pd.to_pickle(Portfolio, 'VXX:UVXY')
