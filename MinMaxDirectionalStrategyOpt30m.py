# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 14:48:09 2018

@author: AmatVictoriaCuramIII
"""
#pseudoturtle
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import random as rand
import pandas as pd
from pandas import read_csv
Dataset = pd.DataFrame()
Dataset2 = pd.DataFrame()
#ticker = 'UVXY'
iterations = range(0, 1000)
Counter = 0
Empty = []
s = pd.read_csv('UVXYnew.csv')
s = s[:]
Start = t.time()
Counter = 0
s['LogRet'] = np.log(s['Adj Close']/s['Adj Close'].shift(1)) 
s['LogRet'] = s['LogRet'].fillna(0) 
s = s[:-280]
for i in iterations:
    Counter = Counter + 1
    nday = rand.randint(3,50)
    hold = rand.randint(3,50)
    ranger = range(0, hold)      
    s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
    s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()
    s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
    s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)
#    s['OriginalTrade'] = 0
#    s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1 
#    s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = -1 
    for r in ranger:
        s['Regime'] = np.where(s['Regime'].shift(1) == -1, -1, s['Regime'])
    
    s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
    s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
#    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > .6:
        continue
    dailyreturn = s['Strategy'].mean()
    dailyvol = s['Strategy'].std()
    if dailyvol == 0: 
        continue
    sharpe =(dailyreturn/dailyvol)
    print(Counter)
    Empty.append(nday)
    Empty.append(hold)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[2]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[2]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[2]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])
    
    
nday = int(Dataset[kfloat][0])
hold = int(Dataset[kfloat][1])
ranger = range(0, hold)
s['ndaymin'] = s['Adj Close'].rolling(window=nday, center=False).min()
s['ndaymax'] = s['Adj Close'].rolling(window=nday, center=False).max()
s['Regime'] = np.where(s['Adj Close'] > s['ndaymax'].shift(1), 1, 0)
s['Regime'] = np.where(s['Adj Close'] < s['ndaymin'].shift(1), -1, 0)
s['OriginalTrade'] = 0
s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == 1)] = 1 
#s['OriginalTrade'].loc[(s['Regime'].shift(1) == 0) & (s['Regime'] == -1)] = -1 
for r in ranger:
    s['Regime'] = np.where(s['Regime'].shift(1) == 1, 1, s['Regime'])

s['Strategy'] = s['Regime'].shift(1) * s['LogRet']
s['Multiplier'] = s['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)
dailyreturn = s['Strategy'].mean()

dailyvol = s['Strategy'].std()
sharpe =(dailyreturn/dailyvol)    
print(MaxDD)
s['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
                                     
                