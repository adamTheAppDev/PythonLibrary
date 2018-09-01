# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:29:15 2017

@author: AmatVictoriaCuramIII
"""

#Dynamic Weighting

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

Ticker1 = 'UVXY' #Short Position
Ticker2 = 'VXX' #Long Position

#Grab local data

Asset1 = DatabaseGrabber(Ticker1)
Asset2 = DatabaseGrabber(Ticker2)

##Grab data post request

#Asset1 = YahooGrabber(Ticker1)
#Asset2 = YahooGrabber(Ticker2)

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

#Asset1 = Asset1[-100:]
#Asset2 = Asset2[-100:]

#Log Returns
#
Asset1['LogRet'] = np.log(Asset1['Adj Close']/Asset1['Adj Close'].shift(1))
Asset1['LogRet'] = Asset1['LogRet'].fillna(0)
Asset2['LogRet'] = np.log(Asset2['Adj Close']/Asset2['Adj Close'].shift(1))
Asset2['LogRet'] = Asset2['LogRet'].fillna(0)
#
##Brute Force Optimization
#
iterations = range(0, 200)
for i in iterations:
    Counter = Counter + 1
    a = rand.random()
    b = 1 - a
    c = 1.5 - (rand.random() * 3 )
    d = b - rand.random()
    e = 4 - (rand.random() * 8 )
    f = b - rand.random()
    
    if abs(c) > abs(e):
        continue

    Asset1['Position'] = a
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Asset1Position = a
    Asset2Position = b
    Portfolio['Asset1Pass'] = (Asset1['Pass']) 
    Portfolio['Asset2Pass'] = (Asset2['Pass'])
    Portfolio['LongShort'] = (Portfolio['Asset1Pass'] * -1) + (Portfolio['Asset2Pass']) #Pass a short position
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Stats
    DailyReturn = Portfolio['LongShort'].mean()
#    if DailyReturn < .0025:
#        continue
    DailyVol = Portfolio['LongShort'].std()
    if Portfolio['LongShort'].std() == 0:
        continue
    Sharpe = (DailyReturn/DailyVol)
    DrawDown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    Portfolio['DrawDown'] = DrawDown
    MaxDD = max(DrawDown)
#    if MaxDD > .25:
#        continue
#    if MaxDD < .05:
#        continue
    AvgDrawDown = Portfolio['DrawDown'].mean()
    StdDrawDown = Portfolio['DrawDown'].std()

#Graph
#Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))

#New Allocation 
    Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (+/-c*StdDrawDown), 
                   (c * StdDrawDown)), (Asset1Position + d), Asset1['Position']) #d
    Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #e (+/-e*StdDrawDown), 
                   (e * StdDrawDown)), (Asset1Position + f), Asset1['Position'])



    Portfolio['NewAsset2Position'] = 1 - Portfolio['NewAsset1Position'] #    np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (AvgDrawDown (+/-c*StdDrawDown)), 
#                    (c * StdDrawDown)), (Asset2Position + e), Asset2['Position']) #e
    
    Portfolio['Asset1NewPass'] = (Asset1['LogRet'] * Portfolio['NewAsset1Position'])                            
    Portfolio['Asset2NewPass'] = (Asset2['LogRet'] * Portfolio['NewAsset2Position'])
    
    Portfolio['NewLongShort'] = (Portfolio['Asset1NewPass'] * -1) + (Portfolio['Asset2NewPass']) #Pass a short position
    Portfolio['NewMultiplier'] = Portfolio['NewLongShort'].cumsum().apply(np.exp)

#Stats
    NewDailyReturn = Portfolio['NewLongShort'].mean()
#    if NewDailyReturn < DailyReturn:
#        continue
#    if NewDailyReturn < .0025:
#        continue
    NewDailyVol = Portfolio['NewLongShort'].std()
#    if Portfolio['NewLongShort'].std() == 0:    
#        continue
    NewSharpe =(NewDailyReturn/(NewDailyVol))
    NewDrawDown =  1 - Portfolio['NewMultiplier'].div(Portfolio['NewMultiplier'].cummax())
    Portfolio['NewDrawDown'] = NewDrawDown
    NewMaxDD = max(NewDrawDown)
#    if NewMaxDD > .25:
#        continue
#    if NewMaxDD < .12:
#        continue
    NewAvgDrawDown = Portfolio['NewDrawDown'].mean()
    NewStdDrawDown = Portfolio['NewDrawDown'].std()

#Graph
#Portfolio['NewLongShort'][:].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))
                                 
    print(Counter) 
    Empty.append(a)
    Empty.append(b)
    Empty.append(c)
    Empty.append(d)
    Empty.append(e)  
    Empty.append(f)  
    Empty.append(Sharpe)
    Empty.append(Sharpe/MaxDD)
    Empty.append(DailyReturn/MaxDD)
    Empty.append(MaxDD)
    Empty.append(NewSharpe)
    Empty.append(NewSharpe/NewMaxDD)
    Empty.append(NewDailyReturn/NewMaxDD)
    Empty.append(NewMaxDD)
    Emptyseries = pd.Series(Empty)
    Dataset[i] = Emptyseries.values
    Empty[:] = [] 
#    
#Out of Loop Data Arrangement
z1 = Dataset.iloc[11]
w1 = np.percentile(z1, 80)
v1 = [] #this variable stores the Nth percentile of top performers
DS1W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z1:
    if h > w1:
      v1.append(h)
for j in v1:
      r = Dataset.columns[(Dataset == j).iloc[11]]    
      DS1W = pd.concat([DS1W,Dataset[r]], axis = 1)
y = max(z1)
k = Dataset.columns[(Dataset == y).iloc[11]] #this is the column number
kfloat = float(k[0])
End = t.time()
print(End-Start, 'seconds later')
print(Dataset[k])
                                 
#Out of Loop Testing                    
Asset1['Position'] = (Dataset[kfloat][0]) #a
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1]) #b
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
Asset1Position = Dataset[kfloat][0]#a
Asset2Position = Dataset[kfloat][1]#b
Portfolio['Asset1Pass'] = (Asset1['Pass']) 
Portfolio['Asset2Pass'] = (Asset2['Pass'])
Portfolio['LongShort'] = (Portfolio['Asset1Pass'] * -1) + (Portfolio['Asset2Pass']) #Pass a short position
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)

#Stats
DailyReturn = Portfolio['LongShort'].mean()
#    if dailyreturn < .0015:
#        continue
DailyVol = Portfolio['LongShort'].std()
#   if Portfolio['LongShort'].std() == 0:    
#        continue
Sharpe = (DailyReturn/DailyVol)
DrawDown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
Portfolio['DrawDown'] = DrawDown
MaxDD = max(DrawDown)
AvgDrawDown = Portfolio['DrawDown'].mean()
StdDrawDown = Portfolio['DrawDown'].std()

#Graph
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))

#New Allocation 
Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #c (+/-Dataset[kfloat][2]*StdDrawDown), 
                (Dataset[kfloat][2]*StdDrawDown)
                ), (Asset1Position + Dataset[kfloat][3]), Asset1['Position'])#d, Dataset[kfloat][3]
Portfolio['NewAsset1Position'] = np.where(Portfolio['DrawDown'].shift(1) > (AvgDrawDown + #e (+/-e*StdDrawDown), 
                (Dataset[kfloat][4]*StdDrawDown)
                ), (Asset1Position + Dataset[kfloat][5]), Asset1['Position'])#d, Dataset[kfloat][3]
Portfolio['NewAsset2Position'] = 1 - Portfolio['NewAsset1Position'] #np.where(Portfolio['DrawDown'] > (AvgDrawDown + #e (AvgDrawDown (+/-Dataset[kfloat][4]*StdDrawDown)), 
                #(Dataset[kfloat][4]*StdDrawDown)
                #), (Asset2Position + Dataset[kfloat][5]), Asset2['Position']) #Dataset[kfloat][5]

Portfolio['Asset1NewPass'] = (Asset1['LogRet'] * Portfolio['NewAsset1Position'])                            
Portfolio['Asset2NewPass'] = (Asset2['LogRet'] * Portfolio['NewAsset2Position'])

Portfolio['NewLongShort'] = (Portfolio['Asset1NewPass'] * -1) + (Portfolio['Asset2NewPass']) #Pass a short position
Portfolio['NewMultiplier'] = Portfolio['NewLongShort'].cumsum().apply(np.exp)

#Stats
NewDailyReturn = Portfolio['NewLongShort'].mean()
#    if dailyreturn < .0015:
#        continue
NewDailyVol = Portfolio['NewLongShort'].std()
#   if Portfolio['NewLongShort'].std() == 0:    
#        continue
NewSharpe =(NewDailyReturn/(NewDailyVol))
NewDrawDown =  1 - Portfolio['NewMultiplier'].div(Portfolio['NewMultiplier'].cummax())
Portfolio['NewDrawDown'] = NewDrawDown
NewMaxDD = max(NewDrawDown)
NewAvgDrawDown = Portfolio['NewDrawDown'].mean()
NewStdDrawDown = Portfolio['NewDrawDown'].std()

#Ratios
Portfolio['VXXDeltaWeight'] = Portfolio['NewAsset1Position'] / (
                 Portfolio['NewAsset1Position']+Portfolio['NewAsset2Position'])
Portfolio['ScaleFactor'] = (Portfolio['NewAsset1Position']+
                            Portfolio['NewAsset2Position'])
#Graph
Portfolio['NewLongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                 figsize=(8,5))    
                
##pd.to_pickle(Portfolio, 'DynamicVolArb')
                
#Tester
#tester = pd.DataFrame()
#tester['BWeight'] = Portfolio['VXXDeltaWeight']
#tester['AWeight'] = 1 - tester['BWeight'] 
#tester['BPass'] = tester['BWeight'] * Asset2['LogRet']
#tester['APass'] = tester['AWeight'] * Asset1['LogRet']
#tester['LongShort'] = tester['APass'] + tester['BPass']
#tester['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
#                                 figsize=(8,5))    