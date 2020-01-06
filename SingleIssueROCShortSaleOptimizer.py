# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:13:31 2019

@author: AmatVictoriaCuramIII
"""

#N Period Edge Ratio Computation

#Import-ant
from YahooGrabber import YahooGrabber
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
import random as rand
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
 
#Let's go
start = t.time()
Counter = 0
#Empty structures
tempdf = pd.DataFrame()
edgelist = []
Empty = []
Dataset = pd.DataFrame()
#Variable assignment

#Issue selection
ticker = 'UVXY'

#Data import
Asset = YahooGrabber(ticker)


iterations = range(0,1000) 

#Trimmer for convenience
Asset = Asset[:]

#Represent index as column in Asset the DataFrame
Asset['Index'] = Asset.index
#Alternative range based index starting from 1, not 0
Asset['RangeIndex'] = range(1, len(Asset.index) + 1)

#Format for mpl - graphics
Asset['IndexToNumber'] = Asset['Index'].apply(mdates.date2num)

#Format Dataframe to feed candlestick_ohlc() - graphics
AssetCopy = Asset[['IndexToNumber', 'Open', 'High', 'Low', 'Close', 'Adj Close']].copy()

#Need to subtract one from this value
Asset['LogRet'] = np.log(Asset['Adj Close']/Asset['Adj Close'].shift(1)) 
Asset['LogRet'] = Asset['LogRet'].fillna(0)

for n in iterations:
    ROC = -.000001 + (rand.random() * 2)
    ROCWindow = rand.randint(10,50)
    HoldPeriod = rand.randint(20,150)
    #ROC calculation
    Asset['RateOfChange'] = (Asset['High'] - Asset['Adj Close'].shift(ROCWindow)
                                  ) / Asset['Adj Close'].shift(ROCWindow)
    #Directional methodology
    Asset['Regime'] =  np.where(Asset['RateOfChange'] >  ROC, -1, np.nan)
    Asset['Regime'] = Asset['Regime'].ffill(limit = HoldPeriod)
    Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
    Asset['Strategy'] = Asset['Strategy'].fillna(0)
    Asset['Multiplier'] = Asset['Strategy'].cumsum().apply(np.exp)
    drawdown =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())
    Asset['drawdown'] =  1 - Asset['Multiplier'].div(Asset['Multiplier'].cummax())

    MaxDD = max(drawdown)


    dailyreturn = Asset['Strategy'].mean()

    dailyvol = Asset['Strategy'].std()
    if dailyvol == 0:
        continue
    sharpe =(dailyreturn/dailyvol)
    
    Counter = Counter + 1
#    if MaxDD > .59:
#        continue
    dailyreturn = Asset['Strategy'].mean()
#    if dailyreturn < 0.0085:
#        continue

    Sharpe = dailyreturn/dailyvol
    SharpeOverMaxDD = Sharpe/MaxDD
    Empty.append(ROC)
    Empty.append(ROCWindow)
    Empty.append(HoldPeriod)
    Empty.append(dailyreturn)
    Empty.append(dailyvol)
    Empty.append(Sharpe)
    Empty.append(SharpeOverMaxDD)
    Empty.append(MaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[n] = Emptyseries.values
    Empty[:] = [] 
    print(Counter)

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
#print(End-Start, 'seconds later')
print(Dataset[k])

ROC = Dataset[kfloat][0]
ROCWindow = Dataset[kfloat][1]
HoldPeriod = Dataset[kfloat][2]
#ROC calculation
Asset['RateOfChange'] = (Asset['Adj Close'] - Asset['Adj Close'].shift(ROCWindow)
                              ) / Asset['Adj Close'].shift(ROCWindow)
#Directional methodology
Asset['Regime'] =  np.where(Asset['RateOfChange'] >  ROC, -1, np.nan)
#Hold it..
Asset['Regime'] = Asset['Regime'].ffill(limit = HoldPeriod)
Asset['Strategy'] = (Asset['Regime']).shift(1)*Asset['LogRet']
Asset['Strategy'] = Asset['Strategy'].fillna(0)

Asset[['LogRet','Strategy']].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))