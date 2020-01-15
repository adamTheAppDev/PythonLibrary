# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

#This is a strategy tester with a brute force optimizer

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

#Input

Ticker1 = 'UVXY'
#Ticker2 = '^VIX'

#Remote Signal
#Ticker3 = '^VIX'

#Here we go
#30MinUVXY
#Asset1 = pd.read_csv('UVXYnew.csv')

#Daily UVXY
Asset1 = YahooGrabber(Ticker1)

#For CC futures csv
#Asset2 = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\VX1CC.csv', sep = ',')
#Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
#Asset2 = Asset2.set_index('Date')
#Asset2 = Asset2.reindex(index=Asset2.index[::-1])


#Out of Sample Selection
Asset1 = Asset1[:-8]

##Log Returns
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)

#Brute Force Optimization
iterations = range(0, 1000)
for i in iterations:
    Counter = Counter + 1
    a = 1
    c = 0#rand.random()
    e = 98#rand.randint(8,100)
    window = int(e)
    Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
    Asset1['Regime'] = np.where(Asset1['MA'] < Asset1['Adj Close'], 1 , -1)                                 
    Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'])
    #if Asset1['Strategy'].std() == 0:    
    #    continue
    
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > float(.721): 
            continue
    
    dailyreturn = Asset1['Strategy'].mean()
    #    if dailyreturn < .003:
    #        continue
    
    dailyvol = Asset1['Strategy'].std()
    sharpe =(dailyreturn/dailyvol)
        
#Asset1['Strategy'][:].cumsum().apply(np.exp).plot(grid=True,
#                                     figsize=(8,5))
    print(Counter)
    Empty.append(a)
    Empty.append(c)
    Empty.append(e)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])

window = int((Dataset[kfloat][2]))
Asset1['MA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()   
Asset1['Regime'] = np.where(Asset1['MA'] < Asset1['Adj Close'], 1 , -1)
Asset1['Strategy'] = (Asset1['LogRet'] * Asset1['Regime'])
Asset1['Strategy'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())

print(max(drawdown))
