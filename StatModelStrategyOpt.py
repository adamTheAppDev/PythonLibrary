# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 23:28:42 2018

@author: AmatVictoriaCuramIII
"""

#This is a strategy model with a brute force optimizer + z score based signal

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

Ticker1 = 'UVXY'

Asset1 = pd.read_csv('UVXYnew.csv')
#Asset1 = YahooGrabber(Ticker1)
Asset1 = Asset1[:-252]
iterations = range(0, 2000)
for i in iterations:
    Counter = Counter + 1
    a = rand.randint(2,30)
    b = 3 - rand.random()*6
    c = rand.randint(2,30)
    Rollwindow = a
    Zscorethreshold = b
    hold = c
    ranger = range(0, hold)
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset1['LogRet+1'] = Asset1['LogRet'] + 1
    meanreturn = Asset1['LogRet'].mean()
    stdreturn = Asset1['LogRet'].std()
    Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
    Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
    rollmeanreturn = Asset1['RollingRet'].mean()
    rollstdreturn = Asset1['RollingRet'].std()
    Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn
    Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                    -1, 0)
    Asset1['Regime'] = np.where(Asset1['RollingZscore'] < (-Zscorethreshold * rollstdreturn),
                                    1, 0)
    for r in ranger:
        Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
        Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == 1, 1, Asset1['Regime'])
#    Asset1['OriginalTrade'] = 0
#    Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1 
#    Asset1['MaxDaily'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).max()
#    Asset1['Position'] = Asset1['MaxDaily']
    Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet']# * Asset1['Position']
    Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    drawdown = drawdown.fillna(0)
#    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > .6:
        continue
    dailyreturn = Asset1['Strategy'].mean()
    dailyvol = Asset1['Strategy'].std()
#    if dailyvol == 0: 
#        continue
    sharpe =(dailyreturn/dailyvol)
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
    
    
Rollwindow = int(Dataset[kfloat][0])
Zscorethreshold = Dataset[kfloat][1]
hold = int(Dataset[kfloat][3])
ranger = range(0, hold)
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['LogRet+1'] = Asset1['LogRet'] + 1
meanreturn = Asset1['LogRet'].mean()
stdreturn = Asset1['LogRet'].std()
Asset1['Zscore'] = (Asset1['LogRet'] - meanreturn)/stdreturn
Asset1['RollingRet'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).mean()
rollmeanreturn = Asset1['RollingRet'].mean()
rollstdreturn = Asset1['RollingRet'].std()
Asset1['RollingZscore'] = (Asset1['RollingRet'] - rollmeanreturn)/rollstdreturn
Asset1['Regime'] = np.where(Asset1['RollingZscore'] > (Zscorethreshold * rollstdreturn),
                                -1, 0)
#Asset1['Regime'] = np.where(Asset1['RollingZscore'] < (-Zscorethreshold * rollstdreturn),
#                                 1, 0)
for r in ranger:
    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == -1, -1, Asset1['Regime'])
#    Asset1['Regime'] = np.where(Asset1['Regime'].shift(1) == 1, 1, Asset1['Regime'])
Asset1['OriginalTrade'] = 0
Asset1['OriginalTrade'].loc[(Asset1['Regime'].shift(1) == 0) & (Asset1['Regime'] == -1)] = -1
#Asset1['MaxDaily'] = Asset1['LogRet'].rolling(window = Rollwindow, center = False).max()
#Asset1['Position'] = Asset1['MaxDaily'] 
Asset1['Strategy'] = Asset1['Regime'].shift(1) * Asset1['LogRet'] #* Asset1['Position']
Asset1['Multiplier'] = Asset1['Strategy'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
drawdown = drawdown.fillna(0)
#    s['drawdown'] =  1 - s['Multiplier'].div(s['Multiplier'].cummax())
MaxDD = max(drawdown)
dailyreturn = Asset1['Strategy'].mean()
dailyvol = Asset1['Strategy'].std()
sharpe =(dailyreturn/dailyvol)
print(MaxDD)    
Asset1['Strategy'].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
