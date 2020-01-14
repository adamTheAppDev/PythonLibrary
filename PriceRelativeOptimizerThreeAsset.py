# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

#This is a three asset portfolio/strategy tester

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

#Input

Ticker1 = 'UVXY'
Ticker2 = 'VXX'
Ticker3 = '^VIX'

#Here we go
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)
Asset3 = YahooGrabber(Ticker3)
#Asset1 = Asset1[-1490:]
#Match lengths

trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]

#Trimmer
Asset3 = Asset3[-len(Asset2):]
#Asset1 = Asset1[-20:]
#Asset2 = Asset2[-20:]

#Log Returns

Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)
#Brute Force Optimization

iterations = range(0, 4000)
for i in iterations:
    Counter = Counter + 1
    a1 = rand.random()
    b1 = rand.random()
    c1 = rand.random()
    total = a1 + b1 + c1
    a = a1/total
    b = b1/total
    if b > .3:
        continue
    c = c1/total
    Asset1['Position'] = a
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Asset3['Position'] = c
    Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass'])
    Portfolio['Asset3Pass'] = (Asset3['Pass'])
#    Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
    #asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']
                               + Portfolio['Asset3Pass']) 
    #    Portfolio['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                         figsize=(8,5))  
    if Portfolio['LongShort'].std() == 0:    
        continue
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > float(.27): 
        continue
    
    dailyreturn = Portfolio['LongShort'].mean()
    if dailyreturn < .0035:
        continue
    
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    print(Counter)
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[4]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[4]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[4]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])




Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Asset3['Position'] = (Dataset[kfloat][2])
Asset3['Pass'] = (Asset3['LogRet'] * Asset3['Position'])
Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass']
Portfolio['Asset3Pass'] = Asset3['Pass']
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']  
                            + Portfolio['Asset3Pass'])
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
#conversionfactor = Portfolio['PriceRelative'][-1]
print(max(drawdown2))
#pd.to_pickle(Portfolio, 'VXX:UVXY')
