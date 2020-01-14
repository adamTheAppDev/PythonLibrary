# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

#This is a two asset portfolio/strategy tester with a brute force optimizer - ATR is incorporated in signal

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
Ticker2 = '^VIX'

#Remote Signal
Ticker3 = '^VIX'

#Data requisition
Asset1 = YahooGrabber(Ticker1)
Asset2 = YahooGrabber(Ticker2)

#Remote Signal
Asset3 = YahooGrabber(Ticker3)

#Match lengths

#Trimmer
trim = abs(len(Asset1) - len(Asset2))
if len(Asset1) == len(Asset2):
    pass
else:
    if len(Asset1) > len(Asset2):
        Asset1 = Asset1[trim:]
    else:
        Asset2 = Asset2[trim:]


Asset3 = Asset3[-len(Asset2):]

#Asset2 = Asset2[-600:]

#Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)

#Prepare the remote controller
Asset3['LogRet'] = np.log(Asset3['Adj Close']/Asset3['Adj Close'].shift(1))
Asset3['LogRet'] = Asset3['LogRet'].fillna(0)

#window = 7
##Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
#Asset3['Method1'] = Asset3['High'] - Asset3['Low']
#Asset3['Method2'] = abs((Asset3['High'] - Asset3['Adj Close'].shift(1)))
#Asset3['Method3'] = abs((Asset3['Low'] - Asset3['Adj Close'].shift(1)))
#Asset3['Method1'] = Asset3['Method1'].fillna(0)
#Asset3['Method2'] = Asset3['Method2'].fillna(0)
#Asset3['Method3'] = Asset3['Method3'].fillna(0)
#Asset3['TrueRange'] = Asset3[['Method1','Method2','Method3']].max(axis = 1)
#Asset3['AverageTrueRange'] = (Asset3['TrueRange'].rolling(window = window,
#                                center=False).sum())/window
#
##Retrim Assets
#Asset1 = Asset1[window:]
#Asset2 = Asset2[window:]                             
#Asset3 = Asset3[window:]

#Brute Force Optimization
iterations = range(0, 3000)
for i in iterations:
    Counter = Counter + 1
    a = rand.random()
    b = 1 - a
    c = rand.random()
    d = 1 - c
    e = rand.randint(3,20)
    window = int(e)
    #Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
    Asset3['Method1'] = Asset3['High'] - Asset3['Low']
    Asset3['Method2'] = abs((Asset3['High'] - Asset3['Adj Close'].shift(1)))
    Asset3['Method3'] = abs((Asset3['Low'] - Asset3['Adj Close'].shift(1)))
    Asset3['Method1'] = Asset3['Method1'].fillna(0)
    Asset3['Method2'] = Asset3['Method2'].fillna(0)
    Asset3['Method3'] = Asset3['Method3'].fillna(0)
    Asset3['TrueRange'] = Asset3[['Method1','Method2','Method3']].max(axis = 1)
    Asset3['AverageTrueRange'] = (Asset3['TrueRange'].rolling(window = window,
                                    center=False).sum())/window    
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > (
        Asset3['Adj Close'].shift(e) + Asset3['AverageTrueRange'].shift(1)),
                                    c,a)                                    
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > (
        Asset3['Adj Close'].shift(e) + Asset3['AverageTrueRange'].shift(1)),
                                    d,b) 
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
#    Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
    #asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
    Portfolio['LongShort'] = (Portfolio['Asset1Pass']) + (Portfolio['Asset2Pass']) 
    #    Portfolio['LongShort'][-180:].cumsum().apply(np.exp).plot(grid=True,
#                                         figsize=(8,5))  
    if Portfolio['LongShort'].std() == 0:    
        continue
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > float(.3): 
        continue
    
    dailyreturn = Portfolio['LongShort'].mean()
    if dailyreturn < .002:
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
    Empty.append(d)
    Empty.append(e)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[6]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[6]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[6]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])


window = int((Dataset[kfloat][4]))
#Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
Asset3['Method1'] = Asset3['High'] - Asset3['Low']
Asset3['Method2'] = abs((Asset3['High'] - Asset3['Adj Close'].shift(1)))
Asset3['Method3'] = abs((Asset3['Low'] - Asset3['Adj Close'].shift(1)))
Asset3['Method1'] = Asset3['Method1'].fillna(0)
Asset3['Method2'] = Asset3['Method2'].fillna(0)
Asset3['Method3'] = Asset3['Method3'].fillna(0)
Asset3['TrueRange'] = Asset3[['Method1','Method2','Method3']].max(axis = 1)
Asset3['AverageTrueRange'] = (Asset3['TrueRange'].rolling(window = window,
                                    center=False).sum())/window    
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])

Asset1['Position'] = (Dataset[kfloat][0])

Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > (
            Asset3['Adj Close'].shift(window) + Asset3['AverageTrueRange'].shift(1)),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > (
            Asset3['Adj Close'].shift(window) + Asset3['AverageTrueRange'].shift(1)),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
#Portfolio['PriceRelative'] = Asset1['Adj Close'] / Asset2['Adj Close']
#asone['PriceRelative'][-180:].plot(grid = True, figsize = (8,5))
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
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
