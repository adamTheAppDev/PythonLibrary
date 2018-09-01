# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:07:37 2017

@author: AmatVictoriaCuramIII
"""
import numpy as np
import random as rand
import pandas as pd
import time as t
from DatabaseGrabber import DatabaseGrabber
from YahooGrabber import YahooGrabber
Empty = []
Dataset = pd.DataFrame()
Dataset2 = pd.DataFrame()
Portfolio = pd.DataFrame()
Start = t.time()
Counter = 0

#Input

Ticker1 = 'UVXY'
#Ticker2 = '^VIX'

#Remote Signal
Ticker3 = '^VIX'

#Here we go
Asset1 = YahooGrabber(Ticker1)
#Asset2 = YahooGrabber(Ticker2)


Asset2 = read_csv('C:\\Users\\AmatVictoriaCuramIII\\Desktop\\Python\\VX1CC.csv', sep = ',')
Asset2.Date = pd.to_datetime(Asset2.Date, format = "%m/%d/%Y") 
Asset2 = Asset2.set_index('Date')
Asset2 = Asset2.reindex(index=Asset2.index[::-1])

Asset1 = Asset1[:-6]

#Remote Signal
Asset3 = Asset2
#Asset3 = YahooGrabber(Ticker3)

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

#Primary Brute Force Optimization
iterations = range(0, 7500)
for i in iterations:
    Counter = Counter + 1
    a = rand.random()
    b = 1 - a
    c = 0#rand.random()
    d = 0#rand.random()
    if c + d > 1:
        continue
    e = rand.randint(3,30)
    window = int(e)

    Asset3['MA'] = Asset3['Close'].rolling(window=window, center=False).mean()
    Asset3['MA'] = Asset3['MA'].fillna(0)
    Asset1['Position'] = a
    Asset1['Position'] = np.where(Asset3['Close'].shift(1) > Asset3['MA'].shift(1),
                                    c,a)                                    
    Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
    Asset2['Position'] = b
    Asset2['Position'] = np.where(Asset3['Close'].shift(1) > Asset3['MA'].shift(1),
                                    d,b)
    Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])
    Portfolio['Asset1Pass'] = (Asset1['Pass']) * (-1) #Pass a short position
    Portfolio['Asset2Pass'] = (Asset2['Pass']) #* (-1)
    Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass']
    if Portfolio['LongShort'].std() == 0:    
        continue
    
    Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
    drawdown =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
    MaxDD = max(drawdown)
    if MaxDD > float(.2): 
        continue
#    
    dailyreturn = Portfolio['LongShort'].mean()
    if dailyreturn < .003:
        continue
    
    dailyvol = Portfolio['LongShort'].std()
    sharpe =(dailyreturn/dailyvol)
    
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
    
#primary optimization output sorting
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

#Secondary optimization. Wow. Much involved.
for i in iterations:
    Counter = Counter + 1
    f = rand.randint(31,252)
    g = rand.random() - .3
    if g < .1:
        continue        
    window2 = int(f)
    Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
    Asset3['MA2'] = Asset3['MA2'].fillna(0)
    Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
    Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] > Asset3['MA2'], 1, 0)
    
    Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
    Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])
    
    Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
    #Asset3['SignalReturns'].cumsum().apply(np.exp).plot()
    
    Asset3['Super'] = (Asset3['SignalReturns'] * g ) + Portfolio['LongShort']
    Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
    SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
    SuperDrawdown = SuperDrawdown.fillna(0)
    SuperMaxDD = max(SuperDrawdown)
    superdailyreturn = Asset3['Super'].mean()
#    if dailyreturn > superdailyreturn:
#        continue
    superdailyvol = Asset3['Super'].std()
    supersharpe =(superdailyreturn/superdailyvol)
    print(Counter)
    Empty.append(f)
    Empty.append(g)
    Empty.append(supersharpe)
    Empty.append(superdailyreturn)
    Empty.append(supersharpe/SuperMaxDD)
    Empty.append(superdailyreturn/SuperMaxDD)
    Empty.append(SuperMaxDD) 
    Empty.append(superdailyreturn)
    Emptyseries = pd.Series(Empty)
    Dataset2[0] = Emptyseries.values
    Dataset2[i] = Emptyseries.values
    Empty[:] = [] 
    
#secondary optimization output sorting    
z2 = Dataset2.iloc[2]
w2 = np.percentile(z2, 80)
v2 = [] #this variable stores the Nth percentile of top performers
DS2W = pd.DataFrame() #this variable stores your financial advisors for specific dataset
for h in z2:
    if h > w1:
      v2.append(h)
for j in v2:
      r = Dataset2.columns[(Dataset2 == j).iloc[2]]    
      DS2W = pd.concat([DS2W,Dataset2[r]], axis = 1)
y2 = max(z2)
k2 = Dataset2.columns[(Dataset2 == y2).iloc[2]] #this is the column number
k2float = float(k2[0])
End2 = t.time()
print(End2-Start, 'seconds later')
print('Dataset[k]')
print(Dataset[k])
print('Dataset2[k2]')
print(Dataset2[k2])    
    

window = int((Dataset[kfloat][4]))
window2 = int((Dataset2[k2float][0]))

Asset3['MA'] = Asset3['Adj Close'].rolling(window=window, center=False).mean()   
Asset3['MA'] = Asset3['MA'].fillna(0)
Asset3['MA2'] = Asset3['Adj Close'].rolling(window=window2, center=False).mean()
Asset3['MA2'] = Asset3['MA2'].fillna(0)
Asset1['Position'] = (Dataset[kfloat][0])
Asset1['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][2],Dataset[kfloat][0])
Asset1['Pass'] = (Asset1['LogRet'] * Asset1['Position'])
Asset2['Position'] = (Dataset[kfloat][1])
Asset2['Position'] = np.where(Asset3['Adj Close'].shift(1) > Asset3['MA'].shift(1),
                                    Dataset[kfloat][3],Dataset[kfloat][1])
Asset2['Pass'] = (Asset2['LogRet'] * Asset2['Position'])

Portfolio['Asset1Pass'] = Asset1['Pass'] * (-1)
Portfolio['Asset2Pass'] = Asset2['Pass'] #* (-1)
Portfolio['LongShort'] = Portfolio['Asset1Pass'] + Portfolio['Asset2Pass'] 
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
dailyreturn = Portfolio['LongShort'].mean()
dailyvol = Portfolio['LongShort'].std()
sharpe =(dailyreturn/dailyvol)
Portfolio['Multiplier'] = Portfolio['LongShort'].cumsum().apply(np.exp)
drawdown2 =  1 - Portfolio['Multiplier'].div(Portfolio['Multiplier'].cummax())
print(max(drawdown2))
Asset3['LongVIX'] = np.where(Portfolio['LongShort'] == 0, 1, 0)
Asset3['VIX<MA2'] = np.where(Asset3['Adj Close'] < Asset3['MA2'], 1, 0)

Asset3['VolRegime'] = Asset3['LongVIX'] - Asset3['VIX<MA2']
Asset3['VolRegime'] = np.where(Asset3['VolRegime'] < 0, 0, Asset3['VolRegime'])

Asset3['SignalReturns'] = np.where(Asset3['VolRegime'] == 1, Asset3['LogRet'], 0)
#Asset3['SignalReturns'].cumsum().apply(np.exp).plot()

SuperFactor = Dataset2[k2float][1]
Asset3['Super'] = (Asset3['SignalReturns'] * SuperFactor) + Portfolio['LongShort']
Asset3['SuperMultiplier'] = Asset3['Super'].cumsum().apply(np.exp)
SuperDrawdown = 1 - Asset3['SuperMultiplier'].div(Asset3['SuperMultiplier'].cummax())
SuperDrawdown = SuperDrawdown.fillna(0)
SuperMaxDD = max(SuperDrawdown)
superdailyreturn = Asset3['Super'].mean()
superdailyvol = Asset3['Super'].std()
supersharpe =(superdailyreturn/superdailyvol)
print(SuperMaxDD)
Asset3['SuperMultiplier'][:].plot()
Portfolio['LongShort'][:].cumsum().apply(np.exp).plot(grid=True,
                                     figsize=(8,5))
#pd.to_pickle(Portfolio, 'VXX:UVXY')