# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 19:17:24 2017

@author: AmatVictoriaCuramIII
"""

#doji finder, its sketchy.
#This is a techincal analysis tool and strategy tester

#modules
from YahooGrabber import YahooGrabber
import numpy as np
import random as rand
import pandas as pd
#define tickers
Ticker1 = 'MS'
iterations = range(0, 2000)
Asset1 = YahooGrabber(Ticker1)
Counter = 0
Empty = []
Dataset = pd.DataFrame()
#trimmer
#Asset1 = Asset1[-2000:]
trail = rand.randint(3,40)
trailrange = range(1,trail)
#statistics
for i in iterations:
    window = rand.randint(3,100)
    mag = rand.random()/500
    Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
    Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
    Asset1['SMA'] = Asset1['Adj Close'].rolling(window=window, center=False).mean()
    Asset1['Trend'] = (Asset1['Adj Close']/Asset1['SMA']) - 1
    Asset1['DojiFactor'] = Asset1['Open']/Asset1['Adj Close'] 
    Asset1['MAGN'] = abs(1 - Asset1['DojiFactor'])
    Asset1['Doji?'] = np.where(Asset1['MAGN'] < mag, 1, 0)
    Asset1['Sign'] = np.where(Asset1['Trend'].shift(1) < 0, 1, -1)
    Asset1['Position'] = (Asset1['Doji?'] * Asset1['Sign'])  
    Asset1['AddlPosition'] = 0
    for t in trailrange:
        Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == 1, 1, Asset1['AddlPosition'])
        Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == -1, -1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(1) == 1, 1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(1) == -1, -1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(2) == 1, 1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(2) == -1, -1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(3) == 1, 1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(3) == -1, -1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(4) == 1, 1, Asset1['AddlPosition'])
#    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(4) == -1, -1, Asset1['AddlPosition'])
    Asset1['TotalPosition'] = Asset1['Position'] + Asset1['AddlPosition']
    Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == -2, -1, Asset1['AddlPosition'])
    Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == 2, 1, Asset1['AddlPosition'])
    Asset1['Pass'] = Asset1['TotalPosition'] * Asset1['LogRet'] 
    Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
    Counter = Counter + 1
    print(Counter)
    drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
    dailyreturn = Asset1['Pass'].mean()
    if dailyreturn < 0:
        continue
    dailyvol = Asset1['Pass'].std()
    if Asset1['Pass'].std() == 0:    
        continue
    sharpe =(dailyreturn/dailyvol)
    MaxDD = max(drawdown)

    Empty.append(window)
    Empty.append(mag)
    Empty.append(trail)
    Empty.append(sharpe)
    Empty.append(sharpe/MaxDD)
    Empty.append(dailyreturn/MaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
##find optimal parameters from simulation
z1 = Dataset.iloc[3]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for l in z1:
    if l > w1:
      v1.append(l)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[3]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[3]] #this is the column number
kfloat = float(k[0])

#window = int(Dataset[kfloat][0])
#mag = Dataset[kfloat][1]
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset1['SMA'] = Asset1['Adj Close'].rolling(window=int(Dataset[kfloat][0]), center=False).mean()
Asset1['Trend'] = (Asset1['Adj Close']/Asset1['SMA']) - 1
Asset1['DojiFactor'] = Asset1['Open']/Asset1['Adj Close'] 
Asset1['MAGN'] = abs(1 - Asset1['DojiFactor'])
Asset1['Doji?'] = np.where(Asset1['MAGN'] < Dataset[kfloat][1], 1, 0)
Asset1['Sign'] = np.where(Asset1['Trend'].shift(1) < 0, 1, -1)
Asset1['Position'] = (Asset1['Doji?'] * Asset1['Sign']) 
Asset1['AddlPosition'] = 0
trail = int(Dataset[kfloat][2])
trailrange = range(1,trail)
for t in trailrange:
    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == 1, 1, Asset1['AddlPosition'])
    Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(t) == -1, -1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(1) == 1, 1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(1) == -1, -1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(2) == 1, 1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(2) == -1, -1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(3) == 1, 1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(3) == -1, -1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(4) == 1, 1, Asset1['AddlPosition'])
#Asset1['AddlPosition'] = np.where(Asset1['Position'].shift(4) == -1, -1, Asset1['AddlPosition'])
Asset1['TotalPosition'] = Asset1['Position'] + Asset1['AddlPosition'] 
Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == -2, -1, Asset1['AddlPosition'])
Asset1['TotalPosition'] = np.where(Asset1['TotalPosition'] == 2, 1, Asset1['AddlPosition'])
Asset1['Pass'] = Asset1['TotalPosition'] * Asset1['LogRet'] 
Asset1['Multiplier'] = Asset1['Pass'].cumsum().apply(np.exp)
drawdown =  1 - Asset1['Multiplier'].div(Asset1['Multiplier'].cummax())
dailyreturn = Asset1['Pass'].mean()
dailyvol = Asset1['Pass'].std()
sharpe =(dailyreturn/dailyvol)
MaxDD = max(drawdown)
print(MaxDD)
Asset1['Multiplier'].plot()
print(Dataset[kfloat])
