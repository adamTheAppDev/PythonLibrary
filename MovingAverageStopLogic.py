# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""

#This is an attempt to implement stop losses and profit targets into a trading strategy
#It is not accurate, see DonchianTrendEfficiencyFilterSingleStockSingleFrequency.py for properly constructed model

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

#Here we go
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

#Brute Force Optimization
iterations = range(0, 20)
for i in iterations:
    Counter = Counter + 1
    a = rand.random()
    b = 1 - a
    c = 0
    d = rand.random()
    if abs(c) + abs(d) > 1:
        continue
    e = 1 + rand.random()
    f = 1 - rand.random()
    g = rand.randint(3,20)
    window = int(g)
        
    Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
    Asset3['Price/MA'] = Asset3['Adj Close']/Asset3['MA']
    Asset3['Signal'] = np.where(Asset3['Price/MA'] >= 1, 1, 0)
    Asset3['CumSignal'] = Asset3['Signal'].cumsum() 
    Asset3['CumSignal'].loc[Asset3['CumSignal'] == 0] = 1
    Asset3['CumSignalDiff'] = Asset3['CumSignal'].diff()
    Asset3['CumSignalDiff'] = Asset3['CumSignalDiff'].fillna(0)
    Asset3['Erase'] = np.where(Asset3['Signal'] == Asset3['Signal'].shift(1),
                                         1, 0)
    Asset3['Erase'] = np.where(Asset3['Signal'] == 0,
                                         0, Asset3['Erase'])
    
    Asset3['TriggerSignal'] = Asset3['Signal'] - Asset3['Erase']
    Asset3['LongPrice'] = np.where(Asset3['TriggerSignal'] == 1, Asset3['Adj Close'], 0)
    Asset3['LongPriceFilled'] = Asset3['LongPrice'] 
    Asset3['LongPriceFilled'] = np.where(Asset3['LongPriceFilled'] == 0,
                     Asset3['LongPriceFilled'].shift(1), Asset3['LongPriceFilled'])
    Asset3['LongPriceFilled'] = Asset3['LongPriceFilled'].fillna(0)  
    
    for m in range(0,20):
        Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'].cumsum() > 1) & 
        (Asset3['LongPriceFilled'] == 0) & (Asset3['LongPriceFilled'].shift(-1) == 0
                        )] = Asset3['LongPriceFilled'].shift(1) 
    
    Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'] == 0) & 
        (Asset3['LongPriceFilled'].cumsum() > 1)] = Asset3['LongPriceFilled'].shift(1)
    Asset3['LongPriceFilled'].loc[(Asset3['LongPrice'] != 0) & 
        (Asset3['LongPriceFilled'].cumsum() > 1)] = 0
        
    Asset3['Regime'] = np.where(Asset3['Signal'].shift(1) == 1, 1, 0)
    Asset3['CumRegime'] = Asset3['Regime'].cumsum()
    Asset3['CumRegimeDiff'] = Asset3['CumRegime'].diff()
    Asset3['Counter'] = range(0,len(Asset3))
    Asset3['HighDiff'] = Asset3['High'] / Asset3['LongPriceFilled']
    Asset3['LowDiff'] = Asset3['Low'] / Asset3['LongPriceFilled']
    Asset3 = Asset3.replace([np.inf, -np.inf], np.nan)
    Asset3[['HighDiff', 'LowDiff']] = Asset3[['HighDiff', 'LowDiff']].fillna(1)
    Asset3['RegimeHighDiff'] = 1
    Asset3['RegimeHighDiff'] = np.where(Asset3['Regime'] == 1, Asset3['HighDiff'], 1)
    Asset3['RegimeLowDiff'] = 1
    Asset3['RegimeLowDiff'] = np.where(Asset3['Regime'] == 1, Asset3['LowDiff'], 1)
    Asset3['StopOut'] = 0
    Asset3['StopOut'] = np.where(Asset3['RegimeLowDiff'] < f, (f - 1), 0 )
    Asset3['StopOut'] = np.where(Asset3['StopOut'].shift(1) == Asset3['StopOut'],
                         0, Asset3['StopOut'])
    Asset3['GainOut'] = 0
    Asset3['GainOut'] = np.where(Asset3['RegimeHighDiff'] > e, (e-1), 0 )
    Asset3['GainOut'] = np.where(Asset3['GainOut'].shift(1) == Asset3['GainOut'],
                         0, Asset3['GainOut'])
    
    Regime = Asset3[['Counter','StopOut','GainOut','CumSignalDiff',
                         'CumRegimeDiff']].loc[(Asset3['RegimeLowDiff'] != 1)]
    Regime['NewCounter'] = range(0, len(Regime))
    
    ToDelete = Regime.loc[(Regime['StopOut'] < 0)]
    ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
    ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
    NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
    for y in NewDelete.Counter:
        Asset3['StopOut'].loc[Asset3['Counter'] == y] = 0
        
    Asset3['GainOut'].loc[(Asset3['StopOut'] < 0) & (Asset3['GainOut'] < 0)] = 0
    
    ToDelete = Regime.loc[(Regime['GainOut'] > 0)]
    ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
    ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
    NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
    for y in NewDelete.Counter:
        Asset3['GainOut'].loc[Asset3['Counter'] == y] = 0
    Asset3['Stops'] = Asset3['StopOut'] + Asset3['GainOut']
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    c,a)                                    
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    d,b)
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
    
    Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] + 
                                (Asset3['Stops'] * d))
    print(Counter)
    if Portfolio['LongShort'].std() == 0:    
        continue
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > float(.1): 
        continue
    
    dailyreturn = Portfolio['LongShort'].mean()
    if dailyreturn < .003:
        continue
    
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
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
    Emptyseries = pd.Series(Empty)
    Dataset[0] = Emptyseries.values
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
    
z1 = Dataset.iloc[8]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[8]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[8]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])

a = Dataset[kfloat][0]
b = Dataset[kfloat][1]
c = Dataset[kfloat][2]
d = Dataset[kfloat][3]
e = Dataset[kfloat][4]
f = Dataset[kfloat][5]
g = Dataset[kfloat][6]
window = int(g)
    
Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()
Asset3['Price/MA'] = Asset3['Adj Close']/Asset3['MA']
Asset3['Signal'] = np.where(Asset3['Price/MA'] >= 1, 1, 0)
Asset3['CumSignal'] = Asset3['Signal'].cumsum() 
Asset3['CumSignal'].loc[Asset3['CumSignal'] == 0] = 1
Asset3['CumSignalDiff'] = Asset3['CumSignal'].diff()
Asset3['CumSignalDiff'] = Asset3['CumSignalDiff'].fillna(0)
Asset3['Erase'] = np.where(Asset3['Signal'] == Asset3['Signal'].shift(1),
                                     1, 0)
Asset3['Erase'] = np.where(Asset3['Signal'] == 0,
                                     0, Asset3['Erase'])

Asset3['TriggerSignal'] = Asset3['Signal'] - Asset3['Erase']
Asset3['LongPrice'] = np.where(Asset3['TriggerSignal'] == 1, Asset3['Adj Close'], 0)
Asset3['LongPriceFilled'] = Asset3['LongPrice'] 
Asset3['LongPriceFilled'] = np.where(Asset3['LongPriceFilled'] == 0,
                 Asset3['LongPriceFilled'].shift(1), Asset3['LongPriceFilled'])
Asset3['LongPriceFilled'] = Asset3['LongPriceFilled'].fillna(0)  

for m in range(0,20):
    Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'].cumsum() > 1) & 
    (Asset3['LongPriceFilled'] == 0) & (Asset3['LongPriceFilled'].shift(-1) == 0
                    )] = Asset3['LongPriceFilled'].shift(1) 

Asset3['LongPriceFilled'].loc[(Asset3['LongPriceFilled'] == 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = Asset3['LongPriceFilled'].shift(1)
Asset3['LongPriceFilled'].loc[(Asset3['LongPrice'] != 0) & 
    (Asset3['LongPriceFilled'].cumsum() > 1)] = 0
    
Asset3['Regime'] = np.where(Asset3['Signal'].shift(1) == 1, 1, 0)
Asset3['CumRegime'] = Asset3['Regime'].cumsum()
Asset3['CumRegimeDiff'] = Asset3['CumRegime'].diff()
Asset3['Counter'] = range(0,len(Asset3))
Asset3['HighDiff'] = Asset3['High'] / Asset3['LongPriceFilled']
Asset3['LowDiff'] = Asset3['Low'] / Asset3['LongPriceFilled']
Asset3 = Asset3.replace([np.inf, -np.inf], np.nan)
Asset3[['HighDiff', 'LowDiff']] = Asset3[['HighDiff', 'LowDiff']].fillna(1)
Asset3['RegimeHighDiff'] = 1
Asset3['RegimeHighDiff'] = np.where(Asset3['Regime'] == 1, Asset3['HighDiff'], 1)
Asset3['RegimeLowDiff'] = 1
Asset3['RegimeLowDiff'] = np.where(Asset3['Regime'] == 1, Asset3['LowDiff'], 1)
Asset3['StopOut'] = 0
Asset3['StopOut'] = np.where(Asset3['RegimeLowDiff'] < f, (f - 1), 0 )
Asset3['StopOut'] = np.where(Asset3['StopOut'].shift(1) == Asset3['StopOut'],
                     0, Asset3['StopOut'])
Asset3['GainOut'] = 0
Asset3['GainOut'] = np.where(Asset3['RegimeHighDiff'] > e, (e-1), 0 )
Asset3['GainOut'] = np.where(Asset3['GainOut'].shift(1) == Asset3['GainOut'],
                     0, Asset3['GainOut'])

Regime = Asset3[['Counter','StopOut','GainOut','CumSignalDiff',
                     'CumRegimeDiff']].loc[(Asset3['RegimeLowDiff'] != 1)]
Regime['NewCounter'] = range(0, len(Regime))

ToDelete = Regime.loc[(Regime['StopOut'] < 0)]
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
for y in NewDelete.Counter:
    Asset3['StopOut'].loc[Asset3['Counter'] == y] = 0
    
Asset3['GainOut'].loc[(Asset3['StopOut'] < 0) & (Asset3['GainOut'] < 0)] = 0

ToDelete = Regime.loc[(Regime['GainOut'] > 0)]
ToDelete['CounterDiff'] = ToDelete['Counter'].diff(1)
ToDelete['NewCounterDiff'] = ToDelete['NewCounter'].diff(1)
NewDelete = ToDelete.loc[(ToDelete['CounterDiff'] == ToDelete['NewCounterDiff'])]
for y in NewDelete.Counter:
    Asset3['GainOut'].loc[Asset3['Counter'] == y] = 0
Asset3['Stops'] = Asset3['StopOut'] + Asset3['GainOut']
Asset1['Position'] = a
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                c,a)                                    
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = b
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                d,b)
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)

Portfolio['LongShort'] = (Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] + 
                            (Asset3['Stops'] * d))

Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
MaxDD = max(drawdown)

dailyreturn = Portfolio['LongShort'].mean()

dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)

Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
MaxDD = max(drawdown)
Portfolio['Multiplier'].plot()
